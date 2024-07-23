/** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from '@web/core/network/rpc_service';

publicWidget.registry.ForecastRestriction = publicWidget.Widget.extend({
    selector: '#product_detail',
    start: function () {
        this._super.apply(this, arguments);
        this._checkForecastedQuantity();
    },
    _checkForecastedQuantity: async function () {
        let productId = this._getProductId();
        console.log(productId)
        if (productId) {
            let result = await jsonrpc('/web/dataset/call_kw/product.product/get_forecasted_quantity', {
                model: 'product.product',
                method: 'get_forecasted_quantity',
                args: [productId],
                kwargs: {},
            });

            if (result < 0) {
            console.log(result)
                this._disableAddToCart();
                this._showForecastMessage();
            }
        }
    },
    _getProductId: function () {
        let $productContainer = $('input[name="product_id"]');
        return $productContainer.val();
    },
    _disableAddToCart: function () {
        console.log( $('#add_to_cart'))
        console.log(document.getElementById("add_to_cart").classList)
       document.getElementById("add_to_cart").classList.add('d-none')
        console.log(document.getElementById("add_to_cart").classList)

    },
    _showForecastMessage: function () {
        let message = '<div class="alert alert-warning">The forecasted quantity is less than zero. The Add to cart functionality is disabled js.</div>';
        $('.oe_website_sale').prepend(message);
    },
});

publicWidget.registry.ForecastWishlistRestriction = publicWidget.Widget.extend({
    selector: '.o_wish_add',
    start: function () {
        this._super.apply(this, arguments);
        this._checkForecastedQuantity();
    },
    _checkForecastedQuantity: async function () {
        let productId = this._getProductId();
        console.log(productId)
        if (productId) {
            let result = await jsonrpc('/web/dataset/call_kw/product.product/get_forecasted_quantity', {
                model: 'product.product',
                method: 'get_forecasted_quantity',
                args: [productId],
                kwargs: {},
            });

            if (result < 0) {
                this._disableAddToCart();
                this._showForecastMessage();
            }
        }
    },
    _getProductId: function () {
        let $wishlistContainer = $('input[name="product_id"]');
        return $wishlistContainer.val();
    },
    _disableAddToCart: function () {
        $('.o_wish_add').addClass('disabled').removeAttr('href').attr('aria-disabled', 'true');
    },
    _showForecastMessage: function () {
        let message = '<div class="alert alert-warning">The forecasted quantity is less than zero. The Add to cart functionality is disabled.</div>';
        $('.oe_website_sale').prepend(message);
    },
});
