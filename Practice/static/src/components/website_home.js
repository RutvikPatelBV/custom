/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { WebsitePreview } from '@website/client_actions/website_preview/website_preview';

patch(WebsitePreview.prototype, {
    setup() {
        super.setup();
        this.doubleNumber = 4 * 2;
        console.log("Jay Shree Ram");
        console.log(this.doubleNumber);
        this.customAction=function(){
                console.log("Jay Shree Ram");
        }
    },
    async customAction() {
        console.log("Jay Shree Ram");
    }
});
