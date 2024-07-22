/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.PasswordGeneratorSnippet = publicWidget.Widget.extend({
    selector: '.password-generator-snippet',
    events: {
        'click #generate-password': '_onGeneratePassword',
        'click #copy-password': '_onCopyPassword',
    },
    _onGeneratePassword: function () {
        const charCount = parseInt(this.$('#char-count').val(), 10);
        if (isNaN(charCount) || charCount <= 0) {
            alert('Please enter a valid number of characters.');
            return;
        }
        const password = this._generatePassword(charCount);
        this.$('#generated-password').val(password);
    },
    _generatePassword: function (length) {
        const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()";
        let password = "";
        for (let i = 0; i < length; i++) {
            const randomIndex = Math.floor(Math.random() * charset.length);
            password += charset[randomIndex];
        }
        return password;
    },
    _onCopyPassword: function () {
        const passwordField = this.$('#generated-password');
        passwordField.select();
        document.execCommand('copy');
        alert('Password copied to clipboard!');
    },
});

export default publicWidget.registry.PasswordGeneratorSnippet;
