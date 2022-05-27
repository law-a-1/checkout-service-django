from django.shortcuts import render
import requests
from .models import Cart, Item, Product
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from .serializers import ProductSerializer, ItemSerializer, CartSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class CartViewSet(APIView):

    def get(self, request):
        token = request.headers['Authorization']
        
        r = requests.get('https://auth-law-a1.herokuapp.com/user', headers={"Authorization": token}).json()

        # print(r)
        username = r["username"]
        # username = "sae"

        try:
            cart = Cart.objects.get(username=username)
        except:
            cart = Cart.objects.create(username=username)

        serializer_cart = CartSerializer(instance=cart)
        return Response(serializer_cart.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            token = request.headers['Authorization']
            r = requests.get('https://auth-law-a1.herokuapp.com/user', headers={"Authorization": token}).json()
            username = r["username"]
        except:
            return Response({
                "error": "UNAUTHORIZED",
                "error_message": "You are not authorized"
            }, status=status.HTTP_404_NOT_FOUND)
        # username = "sae"

        try:
            cart = Cart.objects.get(username=username)
        except:
            cart = Cart.objects.create(username=username)
        

        # product = Product.objects.create(**request.POST.dict())
        product_serializer = ProductSerializer(data=request.data)
        product_serializer.is_valid(raise_exception = True)
        product = product_serializer.save()

        item = Item.objects.create(cart=cart, product=product, amount=1, total_price=product.price)

        cart.grand_total += product.price
        cart.save()

        # item_serializer = ItemSerializer(instance=item)
        cart_serializer = CartSerializer(instance=cart)
        return Response(cart_serializer.data)

    def put(self, request):
        print("UPDATING DATA")
        token = request.headers['Authorization']
        
        r = requests.get('https://auth-law-a1.herokuapp.com/user', headers={"Authorization": token}).json()

        username = r["username"]
        # username = "sae"

        try:
            cart = Cart.objects.get(username=username)
        except:
            cart = Cart.objects.create(username=username)

        try:
            product = Product.objects.get(product_id=request.data["product_id"])
            item = Item.objects.get(cart=cart, product=product)
            if request.data["is_add"]:
                item.amount += 1
                cart.grand_total += product.price
                cart.save()
            else:
                item.amount -= 1
                cart.grand_total -= product.price
                cart.save()

                if item.amount == 0:
                    product.delete()
                    return Response({"message": "Product updated!"})

            item.total_price = item.amount * product.price
            item.save()

            return Response({"message": "Product updated!"})
        except:
            return Response({
                "error": "NOT FOUND",
                "error_message": "Product with requested ID not found"
            }, status=status.HTTP_404_NOT_FOUND)
            

    
    def delete(self, request):
        token = request.headers['Authorization']
        
        r = requests.get('https://auth-law-a1.herokuapp.com/user', headers={"Authorization": token}).json()

        username = r["username"]
        # username = "sae"

        print(request.data['product_id'])

        try:
            cart = Cart.objects.get(username=username)
        except:
            cart = Cart.objects.create(username=username)

        try:
            product = Product.objects.get(product_id=request.data['product_id'])
            print("PRODUCT DAN ITEM DAPET")
            item = Item.objects.get(product=product, cart=cart)
            cart.grand_total -= item.total_price
            cart.save()
            product.delete()
            print("PRODUCT DELETED")
            return Response({"message": "Product deleted!"})
        except:
            return Response({
                "error": "NOT FOUND",
                "error_message": "Product with requested ID not found"
            }, status=status.HTTP_404_NOT_FOUND)
            



class CheckoutViewSet(APIView):
    def post(self, request):
        token = request.headers['Authorization']
        
        r = requests.get('https://auth-law-a1.herokuapp.com/user', headers={"Authorization": token}).json()

        username = r["username"]
        # username = "sae"


        try:
            cart = Cart.objects.get(username=username)
        except:
            cart = Cart.objects.create(username=username)

        items = Item.objects.filter(cart=cart)

        # create_order = requests.post('https://URL_order/', headers={"Authorization": token}).json()


        # for item in items:
        #     print("CHECKOUT PRODUCTS:")
        #     print(item.product.product_id)



            # decrement_stock = request.post(f"http://URL/products/{item.product.product_id}/decrement-stock", data={"amount": item.amount})

            # if decrement_stock.status_code == 200:
            # if True:
            #     cart.grand_total -= item.total_price
            #     cart.save()
            #     item.product.delete()
            # else:
            #     pass

        return Response({"message": "Checkout success"})