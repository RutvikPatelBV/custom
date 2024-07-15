/** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.CustomWidget = publicWidget.Widget.extend({
    selector: '.custom-widget-container',
    start: function () {
        this._super.apply(this, arguments);
        this.renderWidgetContent();
    },
    renderWidgetContent: function () {
        this.$el.html(`
            <div class="alert alert-info">
                This is a custom widget!
                <button class="ml-8 btn btn-primary mt-2" id="shopButton">Go to Shop</button>
            </div>
        `);
        this.bindEvents();
    },
    bindEvents: function () {
        this.$('#shopButton').on('click', function () {
            window.location.href = '/shop';
        });
    },
});
