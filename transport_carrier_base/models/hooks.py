from odoo import api, SUPERUSER_ID

def cleanup_obsolete_views(env):
    xml_ids_to_remove = [
        'transport_carrier_base.stock_picking_transport_carrier_delivery_form_view_inherit',
    ]
    for xml_id in xml_ids_to_remove:
        view = env.ref(xml_id, raise_if_not_found=False)
        if view:
            ir_model_data = env['ir.model.data']
            parent_views_ids = env['ir.ui.view'].search([('inherit_id', '=', view.id)])
            if parent_views_ids:
                for parent in parent_views_ids:
                    model_data_id = ir_model_data.search([('display_name', '=', parent.name)]).unlink()
                parent_views_ids.unlink()
            view_model_data = ir_model_data.search([('display_name', '=', view.name)]).unlink()
            view.unlink()
