/** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from '@web/core/network/rpc_service';

publicWidget.registry.ForecastWishlistRestriction = publicWidget.Widget.extend({
    selector: '#o_comparelist_table',
    start: function () {
        this._super.apply(this, arguments);
        this._checkAllForecastedQuantities();
    },
    _checkAllForecastedQuantities: async function () {
        let self = this;
        $('#o_comparelist_table tbody tr').each(async function () {
            let $row = $(this);
            let productId = $row.data('productId');
            if (productId) {
                let result = await jsonrpc('/web/dataset/call_kw/product.product/get_forecasted_quantity', {
                    model: 'product.product',
                    method: 'get_forecasted_quantity',
                    args: [productId],
                    kwargs: {},
                });

                if (result < 0) {
                    self._disableAddToCart($row);
                }
            }
        });
    },
    _disableAddToCart: function ($row) {
        $row.find('.o_wish_add').addClass('disabled').removeAttr('href').attr('aria-disabled', 'true');
        if ($row.find('.o_wish_add').length) {
            this._showForecastMessage();
        }
    },
    _showForecastMessage: function () {
        let message = '<div class="alert alert-warning">The forecasted quantity is less than zero. The Add to cart functionality is disabled for some items.</div>';
        $('.oe_website_sale').prepend(message);
    }
});
