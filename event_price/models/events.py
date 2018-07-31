
from functools import reduce

from odoo import fields, models, _, api
import logging

from odoo.exceptions import Warning

log = logging.getLogger(__name__)

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import time


class event_registration(models.Model):
    """Event Registration"""
    _inherit= 'event.registration'

    event_campus = fields.Many2one(related='event_id.address_id', string="campus", readonly=True)
    event_body = fields.Many2one(related='event_id.event_type_id',string="Professional Body", readonly=True)
    semester = fields.Selection(related='event_id.semester', string='Semester', readonly=True)


class event_event(models.Model):
    """Extends the event model with an extra price fields."""
    _inherit = 'event.event'

    @api.one
    @api.depends('online_registration_ids')
    def get_online_register(self):
        """Get Confirm or uncofirm register value.
        @param ids: List of Event registration type's id
        @param fields: List of function fields(register_current and register_prospect).
        @param context: A standard dictionary for contextual values
        @return: Dictionary of function fields value.
        """
        res = {}
        count = 0
        for event in self.browse(self.id):
            res[event.id] = {}
            for registration in event.online_registration_ids:
                count += 1
            res[event.id] = count
        self.online_register_current = count
        return res

    price = fields.Float('Course Fees', help="Fees of the Course.")
    semester = fields.Selection([('1', '1st Semester'),
                                 ('2', '2nd Semester'), ('3', '3rd Semester')],
                                string='Course Semester', help="Semester in which the course takes place")
    qualification = fields.Many2one('event.qual', string='Qualification Level')
    study = fields.Many2one('event.options', string='Study Options')
    online_registration_ids = fields.One2many('event.online.registration', 'event_id', string='Online Registrations abc',
                                              readonly=False, required=True)
    online_register_current = fields.Float(compute='get_online_register', string='Online Registrations Current',
                                           required=True, default=0, store=True)


class event_qual(models.Model):
    
    _name = 'event.qual'

    name = fields.Char('Qualification Level', size=64, required=True)
    order = fields.Integer(string='Qualification Level Order')


class event_options(models.Model):
    """Study Options for Course"""
    
    _name = 'event.options'

    name =  fields.Char('Study Options', size=64, required=True)
    description = fields.Text('Description')
    order = fields.Integer('Sequence')


class event_feetype(models.Model):
    """Study Options for Course"""
    
    _name = 'event.feetype'

    name = fields.Char(string='Fee Type', size=64, required=True)


class event_online_registration(models.Model):
    """logs all online Registrations"""
    
    _name = 'event.online.registration'

    id = fields.Integer(string='ID')
    event_id = fields.Many2one('event.event', string='Event', required=True, readonly=True )
    partner_id = fields.Many2one('res.partner', string='Partner')
    namee = fields.Char(string='Name')
    email = fields.Char(string='email')


class sale_order(models.Model):
    """Extends the Sale Order with an field for type of enrollment"""

    _inherit = 'sale.order'

    quote_type = fields.Selection([('freequote', 'Free Quote'), ('enrolment', 'Enrolment'),
                                   ('PC Exam', 'PC Exam'), ('CharterBooks', 'CharterBooks')], string='Quote type')
    affiliation = fields.Selection([('1', 'Self Sponsored'), ('2', 'Company')], string= 'Sponsorship')
    campus = fields.Many2one('res.partner', string= 'Campus')
    prof_body = fields.Many2one('event.type', string= 'Professional Body')
    semester = fields.Selection([('1', '1st Semester'), ('2', '2nd Semester'), ('3', '3rd Semester')],
                                string= 'Semester', help="Semester in which the course takes place")
    student_number = fields.Char(string= 'Student No', size=64)
    semester_id = fields.Many2one('event.semester', string= 'Semester')

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(sale_order, self).onchange_partner_id()
        if self.partner_id:
            self.update({'student_number':self.partner_id.student_number})
        return res

    # @api.multi
    # def onchange_partner_id(self, cr, uid, ids, part, context=None):
    #     if not part:
    #         return {'value': {'partner_invoice_id': False, 'partner_shipping_id': False,  'payment_term': False, 'fiscal_position': False}}
    #
    #     part = self.pool.get('res.partner').browse(cr, uid, part, context=context)
    #     addr = self.pool.get('res.partner').address_get(cr, uid, [part.id], ['delivery', 'invoice', 'contact'])
    #     pricelist = part.property_product_pricelist and part.property_product_pricelist.id or False
    #     payment_term = part.property_payment_term and part.property_payment_term.id or False
    #     fiscal_position = part.property_account_position and part.property_account_position.id or False
    #     dedicated_salesman = part.user_id and part.user_id.id or uid
    #     studentno = part.student_number or False
    #     val = {
    #         'partner_invoice_id': addr['invoice'],
    #         'partner_shipping_id': addr['delivery'],
    #         'payment_term': payment_term,
    #         'fiscal_position': fiscal_position,
    #         'user_id': dedicated_salesman,
    #         'student_number':studentno,
    #     }
    #     if pricelist:
    #         val['pricelist_id'] = pricelist
    #     return {'value': val}

    # @api.multi
    # def create(self, cr, uid, vals, context=None):
    #     if vals.get('name','/')=='/':
    #         vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'sale.order') or '/'
    #     if vals.get('partner_id',False):
    #         onchangeResult = self.onchange_partner_id(cr, uid, [], vals['partner_id'], context=None)
    #         vals.update(onchangeResult['value'])
    #     return super(sale_order, self).create(cr, uid, vals, context=context)

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        res = super(sale_order, self).action_invoice_create()

    
    
    @api.model
    def action_invoice_create(self, cr, uid, ids, grouped=False, states=None, date_invoice = False, context=None):
        if states is None:
            states = ['confirmed', 'done', 'exception']
        res = False
        invoices = {}
        invoice_ids = []
        invoice = self.pool.get('account.invoice')
        obj_sale_order_line = self.pool.get('sale.order.line')
        partner_currency = {}
        if context is None:
            context = {}
        # If date was specified, use it as date invoiced, usefull when invoices are generated this month and put the
        # last day of the last month as invoice date
        if date_invoice:
            context['date_invoice'] = date_invoice
        for o in self.browse(cr, uid, ids, context=context):
            currency_id = o.pricelist_id.currency_id.id
            if (o.partner_id.id in partner_currency) and (partner_currency[o.partner_id.id] != currency_id):
                raise Warning(
                    _('Error!'),
                    _('You cannot group sales having different currencies for the same partner.'))

            partner_currency[o.partner_id.id] = currency_id
            lines = []
            for line in o.order_line:
                if line.invoiced:
                    continue
                elif (line.state in states):
                    lines.append(line.id)
            created_lines = obj_sale_order_line.invoice_line_create(cr, uid, lines)
            if created_lines:
                invoices.setdefault(o.partner_id.id, []).append((o, created_lines))
        if not invoices:
            for o in self.browse(cr, uid, ids, context=context):
                for i in o.invoice_ids:
                    if i.state == 'draft':
                        return i.id
        for val in invoices.values():
            if grouped:
                res = self._make_invoice(cr, uid, val[0][0], reduce(lambda x, y: x + y, [l for o, l in val], []), context=context)
                invoice_ref = ''
                for o, l in val:
                    invoice_ref += o.name + '|'
                    self.write(cr, uid, [o.id], {'state': 'progress'})
                    cr.execute('insert into sale_order_invoice_rel (order_id,invoice_id) values (%s,%s)', (o.id, res))
                #remove last '|' in invoice_ref
                if len(invoice_ref) >= 1: 
                    invoice_ref = invoice_ref[:-1]
                invoice.write(cr, uid, [res], {'origin': invoice_ref, 'name': invoice_ref, 'quote_type':o.quote_type})
            else:
                for order, il in val:
                    res = self._make_invoice(cr, uid, order, il, context=context)
                    invoice_ids.append(res)
                    self.write(cr, uid, [order.id], {'state': 'progress'})
                    cr.execute('insert into sale_order_invoice_rel (order_id,invoice_id) values (%s,%s)', (order.id, res))
        return res

    @api.multi
    def _make_invoice(self, cr, uid, order, lines, context=None):
        inv_obj = self.pool.get('account.invoice')
        obj_invoice_line = self.pool.get('account.invoice.line')
        if context is None:
            context = {}
        invoiced_sale_line_ids = self.pool.get('sale.order.line').search(cr, uid, [('order_id', '=', order.id), ('invoiced', '=', True)], context=context)
        from_line_invoice_ids = []
        for invoiced_sale_line_id in self.pool.get('sale.order.line').browse(cr, uid, invoiced_sale_line_ids, context=context):
            for invoice_line_id in invoiced_sale_line_id.invoice_lines:
                if invoice_line_id.invoice_id.id not in from_line_invoice_ids:
                    from_line_invoice_ids.append(invoice_line_id.invoice_id.id)
        for preinv in order.invoice_ids:
            if preinv.state not in ('cancel',) and preinv.id not in from_line_invoice_ids:
                for preline in preinv.invoice_line:
                    inv_line_id = obj_invoice_line.copy(cr, uid, preline.id, {'invoice_id': False, 'price_unit': -preline.price_unit})
                    lines.append(inv_line_id)
        inv = self._prepare_invoice(cr, uid, order, lines, context=context)
        inv['sale_order_id']= order.id
        inv_id = inv_obj.create(cr, uid, inv, context=context)
        data = inv_obj.onchange_payment_term_date_invoice(cr, uid, [inv_id], inv['payment_term'], time.strftime(DEFAULT_SERVER_DATE_FORMAT))
        if data.get('value', False):
            inv_obj.write(cr, uid, [inv_id], data['value'], context=context)
        inv_obj.button_compute(cr, uid, [inv_id])
        return inv_id


class res_partner(models.Model):
    """Extends the res_partner model (mainly for customer in this case) with an extra m2m
       field type of event"""

    _inherit = 'res.partner'

    event_type_id = fields.Many2one('event.type', string= 'Professional Body')
    idpassport = fields.Char(string='ID/Passport No.')
    vat_no_comp = fields.Char(string='VAT No.')
    cq_password = fields.Char(string='Portal Password')
    findout = fields.Selection([
                             ('1', 'Friend or Colleague'),
                             ('2', 'Institute'),
                             ('3', 'Internet Search Engine'),
                             ('4', 'Advertisement'),
                             ('5', 'Other')], string='Find Out')


class sale_order_line(models.Model):
    """Extends the sale.order.line model to add onchange function to that adds the price when event is chosen"""

    _inherit = 'sale.order.line'

    @api.multi
    def create (self,cr,uid,vals,context=None):
         if vals.get('event_id',False):
              event = self.pool.get('event.event').browse(cr,uid,vals['event_id'])
              if not event.pc_exam:
                 vals['name'] = event.name + " - "+event.study.name or " "
         return super(sale_order_line,self).create(cr,uid,vals,context)

    @api.multi
    def event_change(self, cr, uid, ids, event_id, context=None):
        """ when the event is changed the price should be """
        res = {}
        if not event_id:
            return {}

        event_pool =self.pool.get('event.event')
        event = event_pool.browse(cr, uid, event_id, context=context)
        res['price_unit'] = event['price']
        if not event.pc_exam:
            res['name'] = event.name+" - "+event.study.name or ' '
        return {'value': res}


class product(models.Model):

    _inherit = 'product.product'

    fee_ok = fields.Boolean(string='Remmittance Fee', help='Determine if a product is a fee and if its linked to events and qualification levels')
    event_rem = fields.Many2one('event.event', string='Remittance Event ')
    event_type_rem = fields.Many2one('event.type', string='Remittance Course Category')
    event_qual_rem = fields.Many2one('event.qual', string='Remittance Qualification Category')
    event_feetype_rem = fields.Many2one('event.feetype', string='Fee Type')


class event_portal_reg(models.Model):
    """Event Portal Registration"""
    _name = 'event.portal.reg'
      
    prof_body = fields.Many2one('event.type', string='Professional Body')
    campus = fields.Many2one('res.partner', string='Campus')
    course = fields.Many2many('event.event', string='Courses')
    fees = fields.Many2many('product.product', string='Fees')
    spons = fields.Boolean(string='Sponsorship')
    student = fields.Many2one('res.partner', string='Student')
    quotation = fields.Many2one('sale.order', string='Sales Order')
    invoice = fields.Many2one('account.invoice', string='Invoice')
    reg = fields.Many2one('event.registration', string='Event Registration')


class account_invoice_inh(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def _check_for_fees(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
          res[invoice.id] = {}
          for line in invoice.invoice_line:
            if line['product_id']['fee_ok']:
              res[invoice.id] = True
              return res
        res[invoice.id] = False
        return res

    sale_order_id = fields.Many2one('sale.order', 'Sale Order Link')
    paid_body = fields.Boolean('Paid Body')
    fee_on_invoice = fields.Boolean(compute='_check_for_fees',
                                      store=True,
                                      string='Fees on Invoice')
    quote_type = fields.Selection(related='sale_order_id.quote_type', string='Quote type', readonly=True)
    semester = fields.Selection(related='sale_order_id.semester', string='Semester', readonly=True)
    affiliation = fields.Selection(related='sale_order_id.affiliation', string='Sponsorship', readonly=True)
    campus = fields.Many2one(related='sale_order_id.campus', relation='res.partner', string='Campus', readonly=True)
    prof_body = fields.Many2one(related='sale_order_id.prof_body', type='many2one', relation='event.type',
                                string='Prof Body', readonly=True)
    semester_id = fields.Many2one(related='sale_order_id.semester_id', type='many2one',
                                  relation='event.semester', string='Semester', readonly=True)

    @api.multi
    def action_paid_body(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'paid_body': True})
        return True