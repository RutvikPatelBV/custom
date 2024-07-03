/** @odoo-module */
import { registry } from "@web/core/registry";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class CustomerLocationScreen extends Component {
    static template = "custom_pos_screen.CustomerLocationScreen";

    setup() {
        super.setup(...arguments);
        this.pos = usePos();
        this.orm = useService("orm");

        // Initialize states
        this.locations = useState({ value: [] });
        this.selectedLocation = useState({ value: null });

        // Fetch locations when the component is about to start
        onWillStart(async () => {
            const locations = await this.getLocationList();
            this.locations.value = locations;
        });
    }

    async getLocationList() {
        try {
            const locations = await this.orm.call(
                "practice.pos.config.location",
                "search_read",
                [[['id', 'in', this.pos.config.pos_location_ids]], ['id', 'name']]
            );

            // Transform locations into the desired format
            let LocationList = [];
            locations.forEach(function(location) {
                LocationList.push({
                    id: location.id,
                    name: location.name,
                });
            });

            return LocationList;
        } catch (error) {
            console.error('Error fetching locations:', error);
            return [];
        }
    }

    clickLocation(location) {
        const current_order=this.pos.get_order()
        current_order.location=location.name
        console.log(current_order.location)
        this.selectedLocation.value = location;
        this.pos.showScreen('ProductScreen');
    }

    get selectedLocationName() {
        return this.selectedLocation.value ? this.selectedLocation.value.name : 'Customer Location';
    }
}

// Register the component
registry.category("pos_screens").add("CustomerLocationScreen", CustomerLocationScreen);
