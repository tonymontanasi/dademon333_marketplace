import logging

from application.database.models.good import UpdateGood, GoodStock, Good
from application.database.models.posting_good import (
    PostingGoodCancelReason,
    PostingGood,
)
from application.database.models.task import (
    TaskType,
    TaskStatus,
    UpdateTask,
    Task,
)
from application.database.repositories.discount_repository import (
    DiscountRepository,
)
from application.database.repositories.good_repository import GoodRepository
from application.database.repositories.posting_good_repository import (
    PostingGoodRepository,
)
from application.database.repositories.sku_repository import SKURepository
from application.database.repositories.task_repository import TaskRepository
from application.use_cases.goods.dto.move_to_not_found import (
    MoveToNotFoundInputDTO,
)
from application.use_cases.goods.exceptions import GoodNotFound
from application.utils.cost import fetch_good_cost

logger = logging.getLogger(__name__)


class MoveToNotFoundUseCase:
    def __init__(
        self,
        sku_repository: SKURepository,
        good_repository: GoodRepository,
        task_repository: TaskRepository,
        discount_repository: DiscountRepository,
        posting_good_repository: PostingGoodRepository,
    ):
        self.sku_repository = sku_repository
        self.good_repository = good_repository
        self.task_repository = task_repository
        self.discount_repository = discount_repository
        self.posting_good_repository = posting_good_repository

    async def execute(self, input_dto: MoveToNotFoundInputDTO) -> None:
        good_id = input_dto.id
        logger.info(f"Переносим товар {good_id} на сток not_found")

        good = await self.good_repository.get_by_id(good_id)
        if not good or good.is_sold or good.stock == GoodStock.not_found:
            logger.warning("Товар или не найден, или продан, или утерян")
            raise GoodNotFound()

        await self.good_repository.update(
            UpdateGood(
                id=good_id, stock=GoodStock.not_found, is_reserved=False
            )
        )
        logger.info("Обновили stock и is_reserved")

        await self.process_tasks(good)

    async def process_tasks(self, good: Good) -> None:
        tasks = await self.task_repository.get_by_good_id(good.id)
        logger.info(f"Нашли {len(tasks)} задач")

        for task in tasks:
            if task.type == TaskType.placing:
                await self.on_placing_task(task)
            elif task.type == TaskType.picking:
                await self.on_picking_task(task, good)
            else:
                raise ValueError(f"Неизвестный тип задачи {task.type}")

    async def on_placing_task(self, task: Task) -> None:
        if task.status != TaskStatus.in_work:
            logger.info(f"У задачи {task.id} статус {task.status}")
            return

        await self.task_repository.update(
            UpdateTask(id=task.id, status=TaskStatus.canceled)
        )
        logger.info(f"Закрыли задачу на размещение {task.id}")

    async def on_picking_task(self, task: Task, good: Good) -> None:
        if task.status == TaskStatus.canceled:
            logger.info(f"Задача {task.id} на подбор уже закрыта")
            return
        if task.status == TaskStatus.in_work:
            await self.task_repository.update(
                UpdateTask(id=task.id, status=TaskStatus.canceled)
            )
            logger.info(f"Закрыли задачу на подбор {task.id}")

        await self.posting_good_repository.remove_from_posting(
            good_id=good.id,
            posting_id=task.posting_id,
            cancel_reason=PostingGoodCancelReason.not_found,
        )
        logger.info(f"Удалили товар из заказа {task.posting_id}")

        new_good = await self.good_repository.pick_available_by_sku(
            sku_id=good.sku_id,
            stock=good.stock,
        )
        if not new_good:
            logger.info("Нет доступного нового товара")
            return

        cost = await fetch_good_cost(
            good=new_good,
            sku_repository=self.sku_repository,
            discount_repository=self.discount_repository,
        )
        logger.info(f"Подобран новый товар {new_good.id} по цене {cost}")

        await self.posting_good_repository.create(
            PostingGood(
                posting_id=task.posting_id,
                sku_id=task.sku_id,
                good_id=new_good.id,
                good_stock=new_good.stock,
                cost=cost,
            )
        )
        logger.info(f"Добавили новый товар {new_good.id} к заказу")

        await self.task_repository.create(
            Task(
                type=TaskType.picking,
                sku_id=good.sku_id,
                stock=good.stock,
                count=1,
                posting_id=task.posting_id,
                good_id=new_good.id,
            )
        )
        logger.info("Создали новую picking-задачу")
