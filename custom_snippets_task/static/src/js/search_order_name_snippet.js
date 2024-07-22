/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.SearchOrderSnippet = publicWidget.Widget.extend({
    selector: '.search-order-snippet',
    events: {
        'submit #search_form': '_onSubmitSearchForm',
    },
    _onSubmitSearchForm: function (event) {
        event.preventDefault();
        var self = this;
        var searchQuery = this.$('#search_input').val();

        jsonrpc('/sale_order_search', { search_query: searchQuery }).then(function (result) {
            var resultsHtml = '';
            if (result.length > 0) {
                result.forEach(function (order) {
                    let link = order.portal_url;  // Use the URL from the response
                    resultsHtml += `
                        <table class="table">
                            <tr><th>Sale Order Number</th><td><a href="${link}">${order.name}</a></td></tr>
                            <tr><th>Products</th><td>${order.products}</td></tr>
                            <tr><th>Total Amount</th><td>${order.amount_total}</td></tr>
                            <tr><th>Tax</th><td>${order.tax}</td></tr>
                        </table>
                    `;
                });
            } else {
                resultsHtml = '<p>No matching sale orders found.</p>';
            }
            self.$('#search_results').html(resultsHtml);
        }).catch(function (error) {
            console.error('RPC Query Error:', error);
        });
    },
});

export default publicWidget.registry.SearchOrderSnippet;
