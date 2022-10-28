jQuery(document).ready(function(){
    jQuery(document).on('click',".add-to-cart1",function(){
        var _vm=$(this);
        var _index=_vm.attr('data-index');
        var _qty=$(".product-qty-"+_index).val();
        var _productId=$(".product-id-"+_index).val();
        var _productTitle=$(".product-title-"+_index).val();
        var _productPrice=$(".product-price-"+_index).text();
        $.ajax({
            url:'/add-to-cart',
            data:{
                'id':_productId,
                'qty':_qty,
                'title':_productTitle,
                'price':_productPrice
            },
            dataType:'json',
            beforeSend:function(){
                _vm.attr('disabled',true);
            },
            success:function(res){
                $(".cart-list").text(res.total_items);
                _vm.attr('disabled',false);
            }
        });
    });


    jQuery(document).on('click','.update-item',function(){
        _pId=$(this).attr('data-item');
        _pQty=$(".product-qty-"+_pId).val();
        var _vm = $(this);

        $.ajax({
            url:'/update-cart',
            data:{
                'id':_pId,
                'qty':_pQty,
            },
            dataType:'json',
            beforeSend:function(){
                _vm.attr('disabled',true);
            },
            success:function(res){
                _vm.attr('disabled',false);
                $("#cart_page").html(res.data);
            }
        });
    });
    

    $(document).on('click','.delete-item',function(){
        var _pId=$(this).attr('data-item');
        var _vm = $(this);

        $.ajax({
			url:'/delete-from-cart',
			data:{
                'id':_pId,
            },
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
                $(".cart-list").text(res.total_items);
				_vm.attr('disabled',false);
                $("#cart_page").html(res.data);
			}
		});
    });

});