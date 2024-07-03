/** @odoo-module **/

import { Component , useState } from "@odoo/owl";
import { Navbar } from "./navbar";
import { Todoo } from "@oxp/todoo/todoo";
import { Dashboard } from "@oxp/dashboard/dashboard";
import { Contacts } from "@oxp/contact/contact";

export class WebClient extends Component {
  static template = "oxp.WebClient";
  static components = { Navbar  };
  setup() {
    this.apps = [
        { id: "todoo", name: "Todoo", Component: Todoo },
        { id: "dashboard", name: "Dashboard", Component: Dashboard },
        { id: "contacts", name: "Contacts", Component: Contacts },
    ];
    this.state = useState({
      currentApp: this.apps[0],
    });
  }

  selectApp(appId) {
    const newApp = this.apps.find(app => app.id === appId);
    this.state.currentApp = newApp;
  }
}