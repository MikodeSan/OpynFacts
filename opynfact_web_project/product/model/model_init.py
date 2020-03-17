




if __name__ == '__main__':

    from . import models
    # from . import models.ZProduct
    
    mike = ZContact.objects.create(name="Mike")
    dim = ZContact.objects.create(name="Dimitri")
    job = ZContact.objects.create(name="Joby")

    p0 = ZProduct.objects.create(name="Product_a")
    p1 = ZProduct.objects.create(name="Product_b")
    p2 = ZProduct.objects.create(name="Product_c")
    p3 = ZProduct.objects.create(name="Product_d")
    p4 = ZProduct.objects.create(name="Product_e")
