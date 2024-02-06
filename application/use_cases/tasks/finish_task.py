import logging
from typing import assert_never

from application.database.models.acceptance import (
    UpdateAcceptance,
    AcceptanceStatus,
)
from application.database.models.good import Good, UpdateGood
from application.database.models.posting import UpdatePosting, PostingStatus
from application.database.models.posting_good import (
    UpdatePostingGood,
    PostingGoodCancelReason,
)
from application.database.models.task import (
    TaskStatus,
    TaskType,
    Task,
    UpdateTask,
)
from application.database.repositories.acceptance_repository import (
    AcceptanceRepository,
)
from application.database.repositories.good_repository import GoodRepository
from application.database.repositories.posting_good_repository import (
    PostingGoodRepository,
)
from application.database.repositories.posting_repository import (
    PostingRepository,
)
from application.database.repositories.task_repository import TaskRepository
from application.use_cases.goods.try_pick_new_good import TryPickNewGoodUseCase
from application.use_cases.tasks.dto.finish_task import FinishTaskInputDTO
from application.use_cases.tasks.exceptions import TaskNotFound

logger = logging.getLogger(__name__)


class FinishTaskUseCase:
    def __init__(
        self,
        task_repository: TaskRepository,
        good_repository: GoodRepository,
        posting_repository: PostingRepository,
        posting_good_repository: PostingGoodRepository,
        acceptance_repository: AcceptanceRepository,
        picking_use_case: TryPickNewGoodUseCase,
    ):
        self.task_repository = task_repository
        self.good_repository = good_repository
        self.posting_repository = posting_repository
        self.posting_good_repository = posting_good_repository
        self.acceptance_repository = acceptance_repository
        self.picking_use_case = picking_use_case

    async def execute(self, input_dto: FinishTaskInputDTO) -> None:
        logger.info(
            f"Завершение задачи {input_dto.id} со статусом {input_dto.status}"
        )

        task = await self.task_repository.get_by_id(input_dto.id)
        if not task or task.status != TaskStatus.in_work:
            logger.warning("Задача не найдена или уже завершена")
            raise TaskNotFound()

        new_status = TaskStatus(input_dto.status.value)
        await self.task_repository.update(
            UpdateTask(id=task.id, status=new_status)
        )
        logger.info(f"Обновили статус задачи на {new_status.value}")

        match task.type:
            case TaskType.picking:
                await self.on_picking_task(task, new_status)
            case TaskType.placing:
                await self.on_placing_task(task, new_status)
            case _ as task_type:
                assert_never(task_type)

    async def on_picking_task(self, task: Task, status: TaskStatus) -> None:
        match status:
            case TaskStatus.completed:
                await self.on_completed_picking_task(task)
            case TaskStatus.canceled:
                await self.on_canceled_picking_task(task)
            case _ as status:
                assert_never(status)

    async def on_completed_picking_task(self, task: Task) -> None:
        tasks = await self.task_repository.get_by_posting_id(task.posting_id)
        logger.info(f"Найдено {len(tasks)} задач по {task.posting_id}")

        if any([task.status == TaskStatus.in_work]):
            logger.info("Остались задачи в работе")
            return

        await self.posting_repository.update(
            UpdatePosting(id=task.posting_id, status=PostingStatus.sent)
        )
        logger.info("Обновили статус заказа на sent")

        posting_goods = await self.posting_good_repository.get_by_posting_id(
            task.posting_id
        )
        logger.info(f"Нашли {len(posting_goods)} товаров в заказе")

        await self.good_repository.sell_goods(
            [good.good_id for good in posting_goods if not good.cancel_reason]
        )
        logger.info("Обновили is_reserved и is_sold в goods")

    async def on_canceled_picking_task(self, task: Task) -> None:
        posting_goods = (
            await self.posting_good_repository.get_good_from_posting(
                good_id=task.good_id, posting_id=task.posting_id
            )
        )
        logger.info(f"Нашли {len(posting_goods)} записей о товаре в заказе")

        for posting_good in posting_goods:
            if posting_good.cancel_reason:
                continue

            await self.posting_good_repository.update(
                UpdatePostingGood(
                    id=posting_good.id,
                    cancel_reason=PostingGoodCancelReason.task_canceled,
                )
            )
            logger.info("Удалили товар из заказа")

            await self.picking_use_case.execute(posting_good)

    async def on_placing_task(self, task: Task, status: TaskStatus) -> None:
        if task.acceptance_id:
            await self.on_acceptance_placing_task(task, status)
        if task.posting_id:
            await self.on_posting_placing_task(task)
        assert_never(task)

    async def on_acceptance_placing_task(
        self, task: Task, status: TaskStatus
    ) -> None:
        if status == TaskStatus.completed:
            await self.good_repository.bulk_create(
                [
                    Good(
                        sku_id=task.sku_id,
                        stock=task.stock,
                    )
                    for _ in range(task.count)
                ]
            )
            logger.info(f"Добавили {task.count} новых goods на склад")

        tasks = await self.task_repository.get_by_acceptance_id(
            task.acceptance_id
        )
        logger.info(f"Найдено {len(tasks)} задач по {task.acceptance_id=}")

        if any([task.status == TaskStatus.in_work]):
            logger.info("Остались задачи в работе")
            return

        await self.acceptance_repository.update(
            UpdateAcceptance(
                id=task.acceptance_id, status=AcceptanceStatus.completed
            )
        )
        logger.info("Обновили статус acceptance на completed")

    async def on_posting_placing_task(
        self,
        task: Task,
    ) -> None:
        await self.good_repository.update(
            UpdateGood(id=task.good_id, is_reserved=False)
        )
        logger.info(f"Сняли is_reserved с {task.good_id=}")
