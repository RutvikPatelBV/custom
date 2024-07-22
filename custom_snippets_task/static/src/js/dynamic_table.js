/** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.DynamicTableSnippet = publicWidget.Widget.extend({
    selector: '.dynamic-table-snippet',
    start: function () {
        this._super.apply(this, arguments);
        this._fetchData().then(data => this._renderTable(data));
    },
    _fetchData: function () {
        return this._rpc({
            route: '/get_table_data',
        });
    },
    _renderTable: function (data) {
        const $tbody = this.$('tbody');
        $tbody.empty();
        data.forEach(row => {
            const $tr = $('<tr>');
            $tr.append($('<td>').text(row.column1));
            $tr.append($('<td>').text(row.column2));
            $tr.append($('<td>').text(row.column3));
            $tbody.append($tr);
        });
    },
});
