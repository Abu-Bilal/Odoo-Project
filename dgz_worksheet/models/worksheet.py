from odoo import models, fields, api
from odoo.exceptions import UserError


class Dgzworksheetmain(models.Model):
    _name = 'dgz.worksheet.main'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='name', default=lambda self: self.env.user.name)
    date = fields.Date(string='Date', default=fields.Date.today())
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    worksheet_line_ids = fields.One2many('dgz.worksheet.line', 'worksheet_id', string='Work Detail')
    status = fields.Selection([('Checkin', 'Checkin'), ('Checkout', 'Checkout')], default='Checkin', tracking=True)

    def checkout_button(self):
        records = []
        for work in self.worksheet_line_ids:
            if not work.description or not work.project_id or not work.task_id or not work.time:
                raise UserError("All fields must have values")
            else:
                rec = self.env['account.analytic.line'].create({
                    'name': work.description,
                    'project_id': work.project_id.id,
                    'task_id': work.task_id.id,
                    'unit_amount': work.time,
                    'user_id': self.user_id.id,
                })
                records.append(rec)
        if records:
            self.write({'status': 'Checkout'})
        return records

    @api.model
    def get_worksheet_data(self):
        administrator = self.env.user.has_group('dgz_worksheet.ws_administrator')
        today = fields.Date.today()
        worksheet = self.env['dgz.worksheet.main'].search([('date', '=', today)])
        work_details = {}
        for record in worksheet:
            user_id = record.user_id.id
            if administrator or user_id == self.env.user.id:
                if user_id not in work_details:
                    work_details[user_id] = {
                        'user_id': record.user_id.name,
                        'date': record.date,
                        'work_details': [],
                    }
                for detail in record.worksheet_line_ids:
                    work_detail = {
                        'description': detail.description or '',
                        'project_id': detail.project_id.name or '',
                        'task_id': detail.task_id.name or '',
                        'time': detail.time or '',
                        'status': detail.status or '',
                    }
                    work_details[user_id]['work_details'].append(work_detail)
        return list(work_details.values())

    @api.model
    def worksheet_server_action(self):
        user = self.env.user.name
        date = fields.Date.today(self)
        rec = self.search([('date', '=', date), ('user_id', '=', user)], limit=1)
        if rec:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'dgz.worksheet.main',
                'view_mode': 'form',
                'res_id': rec.id,
                'target': 'current',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'dgz.worksheet.main',
                'target': 'current',
            }


class Dgzworksheetline(models.Model):
    _name = 'dgz.worksheet.line'

    worksheet_id = fields.Many2one('dgz.worksheet.main', string='Name')
    description = fields.Text(string='Description', tracking=True)
    project_id = fields.Many2one('project.project', string='Project', tracking=True)
    task_id = fields.Many2one('project.task', string='Task', tracking=True)
    time = fields.Float(string='Time', tracking=True)
    status = fields.Selection([('working', 'working'), ('onhold', 'onhold'), ('done', 'done')], string='Status',
                              default='working', tracking=True)

    @api.onchange('project_id')
    def _onchange_project(self):
        if self.project_id:
            return {'domain': {'task_id': [('project_id', '=', self.project_id.id)]}}
        else:
            return {'domain': {'task_id': []}}

    @api.onchange('task_id')
    def _onchange_task(self):
        if self.task_id:
            self.project_id = self.task_id.project_id.id
