odoo.define('djbc.import_button', function (require) {
    'use strict';

    const ListController = require('web.ListController');
    const viewRegistry = require('web.view_registry');
    const ListView = require('web.ListView');

    const ImportButtonListController = ListController.extend({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                const $importButton = $('<button/>', {
                    type: 'button',
                    class: 'btn btn-secondary o_list_button_import',
                    text: 'Import',
                }).on('click', this._onImportClick.bind(this));
                this.$buttons.find('.o_list_buttons').append($importButton);
            }
        },

        _onImportClick: function () {
            const action = {
                type: 'ir.actions.client',
                tag: 'import',
                params: {
                    model: this.modelName,
                },
            };
            this.do_action(action);
        },
    });

    const ImportButtonListView = ListView.extend({
        config: Object.assign({}, ListView.prototype.config, {
            Controller: ImportButtonListController,
        }),
    });

    viewRegistry.add('djbc_list_with_import', ImportButtonListView);
});
