from fastapi import HTTPException, status


class InvalidGoodSKU(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SKU товара не соответствует SKU в заказе",
        )


class PostingNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Заказ не найден",
        )
