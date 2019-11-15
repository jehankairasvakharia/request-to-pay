from rest_framework.generics import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ItemSerializer, OrderSerializer, InvoiceSerializer
from .models import Item, Order, Invoice


class ItemList(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('id', )


class ItemCreate(CreateAPIView):
    serializer_class = ItemSerializer

    def create(self, request, *args, **kwargs):
        try:
            price = request.data.get("price")
            if price is not None and float(price) <= 0.0:
                raise ValidationError({"price": "Must be above $0.0"})
        except:
            raise ValidationError({"price": "A valid number is required"})
        return super().create(request, *args, **kwargs)


class ItemRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    lookup_field = "id"
    serializer_class = ItemSerializer


class OrderList(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('id', )


class OrderCreate(CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        try:
            quantity = request.data.get("quantity")
            if quantity is not None and int(quantity) <= 0:
                raise ValidationError({"quantity": "Must be above 0"})
        except:
            raise ValidationError({"quantity": "A valid integer is required"})
        return super().create(request, *args, **kwargs)


class OrderRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    lookup_field = "id"
    serializer_class = OrderSerializer


class InvoiceList(ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('id', )


class InvoiceCreate(CreateAPIView):
    serializer_class = InvoiceSerializer

    def create(self, request, *args, **kwargs):
        self._validate_user(request, "driver", "D")
        self._validate_user(request, "customer", "C")

        return super().create(request, *args, **kwargs)

    @staticmethod
    def _validate_user(request, user_role: str, user_type: str):
        try:
            user = request.data.get("user")
            if user is not None and getattr(user, "user_type") != user_type:
                raise ValidationError({user_role: f"Must be a {user_role} user"})
        except:
            raise ValidationError({user_role: "A valid driver is required"})


class InvoiceRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    lookup_field = "id"
    serializer_class = InvoiceSerializer