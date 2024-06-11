/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import PortalSidebar from '@portal/js/portal_sidebar';

PortalSidebar.include({
//    selector: ".o_portal_purchase_sidebar",
//    template: "purchase.portal_my_home_menu_purchase",

    init: function (parent) {
        this._super.apply(this, arguments);
        console.log("Jay Shree Ram");
    },

    start: function () {
        this._super.apply(this, arguments);

        this.$el.css('background-color', '#FFE6E6');
        this.$el.css('border-radius','20px')

        // Use document to query the DOM correctly
        let element = document.querySelector(".col-lg-3.col-xl-4.d-print-none");
        if (element) {
            element.style.backgroundColor = '#E1AFD1';
            element.style.borderTopLeftRadius = '20px';
            element.style.borderBottomLeftRadius = '20px';
            element.addEventListener("click", (event) => {
                console.log("Jay Shree Ram")
                    });
        } else {
            console.warn("Element with class 'col-lg-3 col-xl-4 d-print-none' not found");
        }
        this.$el.on('click', '#redirect_to_contact_us', function() {
            window.location.href = '/contactus';
        });
    }
});
