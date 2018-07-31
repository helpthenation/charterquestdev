# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, models, api, _
from odoo.tools.translate import _
import odoo.addons.decimal_precision as dp


class product_template(models.Model):
    _inherit = 'product.template'

    event_ok = fields.Boolean(string='Event Subscription',
                              help='Determine if a product needs to create automatically an event registration at the confirmation of a sales order line.')
    event_type_id = fields.Many2one('event.type', string='Type of Event', help='Select event types so when we use this product in sales order lines, it will filter events of this type only.')

    @api.multi
    @api.onchange('event_ok')
    def onchange_event_ok(self):
        pass
        # if event_ok:
        #     return {'value': {'type': 'service'}}
        # return {}


class product(models.Model):
    _inherit = 'product.product'
    
    event_ticket_ids = fields.One2many('event.event.ticket', 'product_id', string='Event Tickets')
    # @api.multi
    # def onchange_event_ok(self, event_ok):
    #     # cannot directly forward to product.template as the ids are theoretically different
    #     if event_ok:
    #         return {'value': {'type': 'service'}}
    #     return {}


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    
    event_id = fields.Many2one('event.event', 'Event',
            help="Choose an event and it will automatically create a registration for this event.")
    event_ticket_id = fields.Many2one('event.event.ticket', 'Event Ticket',
            help="Choose an event ticket and it will automatically create a registration for this event ticket.")
        #those 2 fields are used for dynamic domains and filled by onchange
    event_type_id = fields.Many2one(related='product_id.event_type_id', relation="event.type", string="Event Type")
    event_ok = fields.Boolean(related='product_id.event_ok', string='event_ok')

    # @api.multi
    # def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
    #     res = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line,
    #                                                                         account_id=account_id,
    #                                                                         context=context)
    #     if line.event_id:
    #         event = self.pool['event.event'].read(cr, uid, line.event_id.id, ['name'], context=context)
    #         res['name'] = '%s: %s' % (res['name'], event['name'])
    #     return res

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        res = super(sale_order_line, self).product_id_change()
        if self.product_id:
            product_res = self.env['product.product'].browse(self.product_id.id)
            # if product_res.event_ok:
                # res['value'].update(event_type_id=product_res.event_type_id.id,
                #                     event_ok=product_res.event_ok)
            # else:
                # res['value'].update(event_type_id=False,
                #                     event_ok=False)
        return res

    # @api.multi
    # def product_id_change(self, cr, uid, ids,
    #                       pricelist,
    #                       product,
    #                       qty=0,
    #                       uom=False,
    #                       qty_uos=0,
    #                       uos=False,
    #                       name='',
    #                       partner_id=False,
    #                       lang=False,
    #                       update_tax=True,
    #                       date_order=False,
    #                       packaging=False,
    #                       fiscal_position=False,
    #                       flag=False, context=None):
    #     """
    #     check product if event type
    #     """
    #     res = super(sale_order_line,self).product_id_change(cr, uid, ids, pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id, lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)
    #     if product:
    #         product_res = self.pool.get('product.product').browse(cr, uid, product, context=context)
    #         if product_res.event_ok:
    #             res['value'].update(event_type_id=product_res.event_type_id.id,
    #                                 event_ok=product_res.event_ok)
    #         else:
    #             res['value'].update(event_type_id=False,
    #                                 event_ok=False)
    #     return res

    @api.multi
    def button_confirm(self, cr, uid, ids, context=None):
        '''
        create registration with sales order
        '''
        context = dict(context or {})
        registration_obj = self.pool.get('event.registration')
        for order_line in self.browse(cr, uid, ids, context=context):
            if order_line.event_id:
                dic = {
                    'name': order_line.order_id.partner_invoice_id.name,
                    'partner_id': order_line.order_id.partner_id.id,
                    'nb_register': int(order_line.product_uom_qty),
                    'email': order_line.order_id.partner_id.email,
                    'phone': order_line.order_id.partner_id.phone,
                    'origin': order_line.order_id.name,
                    'event_id': order_line.event_id.id,
                    'event_ticket_id': order_line.event_ticket_id and order_line.event_ticket_id.id or None,
                }

                if order_line.event_ticket_id:
                    message = _("The registration has been created for event <i>%s</i> with the ticket <i>%s</i> from the Sale Order %s. ") % (order_line.event_id.name, order_line.event_ticket_id.name, order_line.order_id.name)
                else:
                    message = _("The registration has been created for event <i>%s</i> from the Sale Order %s.") % (order_line.event_id.name, order_line.order_id.name)
                
                context.update({'mail_create_nolog': True})
                registration_id = registration_obj.create(cr, uid, dic, context=context)
                registration_obj.message_post(cr, uid, [registration_id], body=message, context=context)
        return super(sale_order_line, self).button_confirm(cr, uid, ids, context=context)

    @api.multi
    def onchange_event_ticket_id(self, cr, uid, ids, event_ticket_id=False, context=None):
        price = event_ticket_id and self.pool.get("event.event.ticket").browse(cr, uid, event_ticket_id, context=context).price or False
        return {'value': {'price_unit': price}}


class event_event(models.Model):
    _inherit = 'event.event'

    def _default_tickets(self):
        try:
            product = self.env.ref('event_sale.product_product_event')
            return [{
                'name': _('Subscription'),
                'product_id': product.id,
                'price': 0,
            }]
        except ValueError:
            return self.env['event.event.ticket']


    event_ticket_ids = fields.One2many('event.event.ticket', 'event_id', string='Event Ticket',
        default=lambda rec: rec._default_tickets(), copy=True)
#    seats_max = Integer(string='Maximum Available Seats',
#        help="The maximum registration level is equal to the sum of the maximum registration of event ticket. " +
#            "If you have too much registrations you are not able to confirm your event. (0 to ignore this rule )",
#        store=True, readonly=True, compute='_compute_seats_max')

    badge_back = fields.Html('Badge Back', translate=True, states={'done': [('readonly', True)]})
    badge_innerleft = fields.Html('Badge Innner Left', translate=True, states={'done': [('readonly', True)]})
    badge_innerright = fields.Html('Badge Inner Right', translate=True, states={'done': [('readonly', True)]})



 #   @api.one
 #   @api.depends('event_ticket_ids.seats_max')
 #   def _compute_seats_max(self):
 #       self.seats_max = sum(ticket.seats_max for ticket in self.event_ticket_ids)


class event_ticket(models.Model):
    _name = 'event.event.ticket'

    def _get_seats(self):
        """Get reserved, available, reserved but unconfirmed and used seats for each event tickets.
        @return: Dictionary of function field values.
        """
        res = dict([(id, {}) for id in self])
        for ticket in self.browse([]):
            res[ticket.id]['seats_reserved'] = sum(reg.nb_register for reg in ticket.registration_ids if reg.state == "open")
            res[ticket.id]['seats_used'] = sum(reg.nb_register for reg in ticket.registration_ids if reg.state == "done")
            res[ticket.id]['seats_unconfirmed'] = sum(reg.nb_register for reg in ticket.registration_ids if reg.state == "draft")
            res[ticket.id]['seats_available'] = ticket.seats_max - \
                (res[ticket.id]['seats_reserved'] + res[ticket.id]['seats_used']) \
                if ticket.seats_max > 0 else None
        return res

    @api.multi
    def _is_expired(self, cr, uid, ids, field_name, args, context=None):
        # FIXME: A ticket is considered expired when the deadline is passed. The deadline should
        #        be considered in the timezone of the event, not the timezone of the user!
        #        Until we add a TZ on the event we'll use the context's current date, more accurate
        #        than using UTC all the time.
        current_date = fields.date.context_today(self, cr, uid, context=context)
        return {ticket.id: ticket.deadline and ticket.deadline < current_date
                      for ticket in self.browse(cr, uid, ids, context=context)}

    @api.multi
    def _get_price_reduce(self, cr, uid, ids, field_name, arg, context=None):
        res = dict.fromkeys(ids, 0.0)
        for ticket in self.browse(cr, uid, ids, context=context):
            product = ticket.product_id
            discount = product.lst_price and (product.lst_price - product.price) / product.lst_price or 0.0
            res[ticket.id] = (1.0-discount) * ticket.price
        return res

    def _default_product_id(self):

        return self.env.ref('sale.advance_product_0').id

    name = fields.Char('Name', required=True, translate=True)
    event_id = fields.Many2one('event.event', string="Event", required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True,
                                 domain=[("event_type_id", "!=", False)], default=_default_product_id)
    registration_ids = fields.One2many('event.registration', 'event_ticket_id', 'Registrations')
    deadline = fields.Date("Sales End")
    is_expired = fields.Boolean(compute='_is_expired', string='Is Expired')
    price = fields.Float('Price', digits_compute=dp.get_precision('Product Price'))
    price_reduce = fields.Float(compute='_get_price_reduce', string='Price Reduce', digits_compute=dp.get_precision('Product Price'))
    seats_max = fields.Integer('Maximum Available Seats', oldname='register_max', help="You can for each event define a maximum registration level. If you have too much registrations you are not able to confirm your event. (put 0 to ignore this rule )")
    seats_reserved = fields.Integer(compute='_get_seats', string='Reserved Seats')
    seats_available = fields.Integer(compute='_get_seats', string='Available Seats')
    seats_unconfirmed = fields.Integer(compute='_get_seats', string='Unconfirmed Seat Reservations')
    seats_used = fields.Integer(compute='_get_seats', string='Number of Participations')

    @api.multi
    def _check_seats_limit(self, cr, uid, ids, context=None):
        for ticket in self.browse(cr, uid, ids, context=context):
            if ticket.seats_max and ticket.seats_available < 0:
                return False
        return True

    # _constraints = [
    #     (_check_seats_limit, 'No more available tickets.', ['registration_ids','seats_max']),
    # ]

    @api.multi
    def onchange_product_id(self, cr, uid, ids, product_id=False, context=None):
        price = self.pool.get("product.product").browse(cr, uid, product_id).list_price if product_id else 0
        return {'value': {'price': price}}


class event_registration(models.Model):

    """Event Registration"""
    _inherit = 'event.registration'

    event_ticket_id = fields.Many2one('event.event.ticket', 'Event Ticket')

    @api.multi
    def _check_ticket_seats_limit(self, cr, uid, ids, context=None):
        for registration in self.browse(cr, uid, ids, context=context):
            if registration.event_ticket_id.seats_max and registration.event_ticket_id.seats_available < 0:
                return False
        return True

    # _constraints = [
    #     (_check_ticket_seats_limit, 'No more available tickets.', ['event_ticket_id','nb_register','state']),
    # ]