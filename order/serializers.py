from rest_framework import serializers
from .models import Table, Order, OrderItem
from menu.models import MenuItem, Customization

class CustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customization
        fields = ['id', 'name', 'price']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price']

class OrderItemSerializer(serializers.ModelSerializer):

    menu_item = MenuItemSerializer(read_only=True)
    customizations = CustomizationSerializer(many=True, read_only=True)

    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
        source='menu_item',
        write_only=True)

    customizations_id = serializers.PrimaryKeyRelatedField(
        queryset=Customization.objects.all(),
        source='customizations',
        write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id',
                  'menu_item',
                  'menu_item_id',
                  'quantity',
                  'customizations',
                  'customizations_id',
                  'unit_price',
                  'line_total']

class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)
    table_number = serializers.PrimaryKeyRelatedField(
        queryset=Table.objects.all(),
        allow_null=True,
        required=False)

    class Meta:
        model = Order
        fields = ['id',
                  'table_number',
                  'status',
                  'items',
                  'created_at',
                  'updated_at',
                  'notes']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            customization_ids = item_data.pop('customizations', [])
            order_item = OrderItem.objects.create(order=order, **item_data)
            order_item.customizations.set(customization_ids)
            order_item.save()
        return order