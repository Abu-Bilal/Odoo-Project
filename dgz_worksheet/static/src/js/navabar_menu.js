/* @odoo-module */
import core from 'web.core';
import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';
import rpc from 'web.rpc';
var qweb = core.qweb;

const SystrayWidget = Widget.extend({
  template: 'DgzWorksheetDropdown',
  events: {
    'click .o-dropdown': '_onClick',
    'click #worksheet_button': '_onWorksheetClick',
    'click #task_button': '_onTaskClick'
  },
  init: function (parent, options) {
    this._super(parent);
    this.work_detail_ids = '';
    this.loadAllUsersData();
    this.focusWorksheetButton();
  },
  _onClick: function (ev) {
    this.loadAllUsersData();
    let dropBox = $(ev.currentTarget.parentElement).find('#systray_notif');
    if (dropBox.css('display') === 'block') {
      dropBox.css('display', 'none');
    } else {
      dropBox.css('display', 'block');
      this.setupDocumentClickListener(dropBox);
    }
    $('.systray_notification').html(qweb.render("SystrayDetails", { users_data: this.work_detail_ids }));

    this.focusWorksheetButton();
    this.changeHeaderBackgroundColor();
  },
  setupDocumentClickListener: function (dropBox) {
    const self = this;
    const documentClickHandler = function (e) {
      if (!$(e.target).closest('.o-dropdown').length) {
        dropBox.hide();
        $(document).off('click', documentClickHandler);
      }
    };
    $(document).on('click', documentClickHandler);
  },
  _onWorksheetClick: function (ev) {
    ev.stopPropagation();
    this.loadAllUsersData();
    this.focusWorksheetButton();
  },
  _onTaskClick: function (ev) {
    ev.stopPropagation();
    this.loadAllTaskData();
    this.focusTaskButton();
  },

  loadAllUsersData: function () {
    rpc.query({
      model: 'dgz.worksheet.main',
      method: 'get_worksheet_data',
    }).then(result => {
      this.work_detail_ids = result;
      $('.systray_notification').html(qweb.render("SystrayDetails", { users_data: this.work_detail_ids }));

      this.changeHeaderBackgroundColor();
    });
  },

  loadAllTaskData: function () {
    const self = this;
    rpc.query({
       model: 'assign.task',
       method: 'get_user_records',
    }).then(result => {
       self.tasksUser = result;
       $('.systray_notification').html(qweb.render("TaskDetails", { task_data: self.tasksUser }));
    });
  },

  focusWorksheetButton: function () {
    $('#worksheet_button').addClass('active');
    $('#task_button').removeClass('active');
  },
  focusTaskButton: function () {
    $('#task_button').addClass('active');
    $('#worksheet_button').removeClass('active');
  },

  changeHeaderBackgroundColor: function () {
    $('.systray_notification table').each(function () {
      if ($(this).find('.fa-play').length === 0) {
        $(this).find('th').css('background-color', '#5a4f7f');
        $(this).find('th').css('color', '#ffffff');
      }
    });
  },
});

SystrayMenu.Items.push(SystrayWidget);
export default SystrayWidget;
