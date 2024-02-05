import logging
from uuid import UUID

from application.database.models.good import Good, GoodStock, UpdateGood
from application.database.models.posting import Posting
from application.database.models.posting_good import PostingGood
from application.database.models.task import Task, TaskType
from application.database.repositories.discount_repository import (
    DiscountRepository,
)
from application.database.repositories.good_repository import GoodRepository
from application.database.repositories.posting_good_repository import (
    PostingGoodRepository,
)
from application.database.repositories.posting_repository import (
    PostingRepository,
)
from application.database.repositories.sku_repository import SKURepository
from application.database.repositories.task_repository import TaskRepository
from application.use_cases.goods.exceptions import GoodNotFound
from application.use_cases.postings.dto.create_posting import (
    CreatePostingInputDTO,
    CreatePostingOutputDTO,
    CreatePostingGoodInputDTO,
)
from application.use_cases.postings.exceptions import InvalidGoodSKU
from application.use_cases.sku.exceptions import SKUNotFound
from application.utils.cost import get_good_cost

logger = logging.getLogger(__name__)


class CreatePostingUseCase:
    def __init__(
        self,
        sku_repository: SKURepository,
        good_repository: GoodRepository,
        task_repository: TaskRepository,
        discount_repository: DiscountRepository,
        posting_repository: PostingRepository,
        posting_good_repository: PostingGoodRepository,
    ):
        self.sku_repository = sku_repository
        self.good_repository = good_repository
        self.task_repository = task_repository
        self.discount_repository = discount_repository
        self.posting_repository = posting_repository
        self.posting_good_repository = posting_good_repository

    async def execute(
        self, input_dto: CreatePostingInputDTO
    ) -> CreatePostingOutputDTO:
        logger.info(f"Создание заказа с {len(input_dto.ordered_goods)} sku")

        posting = await self.posting_repository.create(Posting())
        logger.info(f"Создан заказ с id {posting.id}")

        for item in input_dto.ordered_goods:
            await self.process_order_item(item, posting.id)

        return CreatePostingOutputDTO(id=posting.id)

    async def process_order_item(
        self, item: CreatePostingGoodInputDTO, posting_id: UUID
    ):
        sku = await self.sku_repository.get_by_id(item.sku)
        if not sku:
            logger.warning(f"SKU {item.sku} не найдена")
            raise SKUNotFound()
        if sku.is_hidden:
            logger.warning(f"SKU {item.sku} не доступна к покупке")
            raise SKUNotFound()
        logger.info(f"SKU {item.id} доступна для покупки")

        sku_discount = await self.discount_repository.get_max_sku_discount(
            sku_id=sku.id
        )
        logger.info(f"Максимальная скидка к товару: {sku_discount}")

        valid_goods = await self.good_repository.get_by_ids(
            item.from_valid_ids
        )
        logger.info(
            f"Найдено {len(valid_goods)} валидных товаров по SKU {sku.id}"
        )

        defect_goods = await self.good_repository.get_by_ids(
            item.from_defect_ids
        )
        logger.info(
            f"Найдено {len(valid_goods)} дефектных товаров по SKU {sku.id}"
        )

        self.validate_goods(valid_goods, item, GoodStock.valid)
        logger.info(f"Провалидировали валидные товары из sku {sku.id}")
        self.validate_goods(defect_goods, item, GoodStock.defect)
        logger.info(f"Провалидировали дефектные товары из sku {sku.id}")

        await self.process_goods(
            goods=valid_goods,
            posting_id=posting_id,
            sku_base_price=sku.base_price,
            sku_discount=sku_discount,
        )
        logger.info("Добавили валидные товары в заказ")
        await self.process_goods(
            goods=defect_goods,
            posting_id=posting_id,
            sku_base_price=sku.base_price,
            sku_discount=sku_discount,
        )
        logger.info("Добавили дефектные товары в заказ")

    async def process_goods(
        self,
        goods: list[Good],
        posting_id: UUID,
        sku_base_price: float,
        sku_discount: float,
    ):
        for good in goods:
            await self.good_repository.update(
                UpdateGood(id=good.id, is_reserved=True)
            )
            logger.info(f"Зарезервировали товар {good.id}")

            cost = get_good_cost(
                sku_base_price=sku_base_price,
                sku_discount=sku_discount,
                good=good,
            )
            logger.info(f"Цена на товар {good.id}: {cost}")

            posting_good = await self.posting_good_repository.create(
                PostingGood(
                    posting_id=posting_id,
                    sku_id=good.sku_id,
                    good_id=good.id,
                    good_stock=good.stock,
                    cost=cost,
                )
            )
            logger.info(f"Товар прикреплён к заказу {posting_good.id}")

            task = await self.task_repository.create(
                Task(
                    type=TaskType.picking,
                    sku_id=good.sku_id,
                    stock=good.stock,
                    count=1,
                    posting_id=posting_id,
                    good_id=good.id,
                )
            )
            logger.info(f"Создали задачу на сборку {task.id}")

    @staticmethod
    def validate_goods(
        goods: list[Good],
        item: CreatePostingGoodInputDTO,
        expected_stock: GoodStock,
    ) -> None:
        if len(goods) != len(item.from_valid_ids):
            logger.info(
                f"В заказе указано {len(item.from_valid_ids)} товаров,"
                f" найдено {len(goods)}"
            )
            raise GoodNotFound()

        for good in goods:
            if good.sku_id != item.sku:
                logger.info(
                    f"У товара {good.id} в заказе указан SKU {item.sku},"
                    f" не соответствует SKU {good.sku_id}"
                )
                raise InvalidGoodSKU()
            if good.stock != expected_stock:
                logger.info(
                    f"У товара {good.id} указан неверный stock: {good.stock},"
                    f" ожидался {expected_stock}"
                )
                raise GoodNotFound()
            if (
                good.is_sold
                or good.is_reserved
                or good.stock == GoodStock.not_found
            ):
                logger.warning("Товар или не найден, или продан, или утерян")
                raise GoodNotFound()
