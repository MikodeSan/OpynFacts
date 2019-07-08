# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 14:14:16 2016

@author: doZan
"""

import sys
import os
import logging as lg

from PyQt5.QtCore import Qt, QItemSelection, QModelIndex, QDateTime
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QAbstractItemView #, QHeaderView, QTreeWidgetItem, QInputDialog

from ui_opynfacts import Ui_Form

# add 'model' package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# add 'database' interface package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_json import ZDataBase_JSON as database


class ZOpynFacts_View(QWidget):

    PROJECT_NONE = "None"
    #    __CREDIT_TREE_DATA_LABEL = ['Label', 'Id.', 'Capital']

    def __init__(self, model, parent=None):

        super(ZOpynFacts_View, self).__init__(parent)

        self.__lg = lg
        self.__lg.basicConfig(level=lg.DEBUG)

        # Model
        self.__model = model

        # view data
        self.__selected_category_lst = []

        # Initialize main UI form
        self.__create_widgets()

        # set model for category view
        self.category_stdmodel = QStandardItemModel()
        self.ui.category_view.setModel(self.category_stdmodel)
        self.ui.category_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # populate category view model
        self.__update_view_category()
        category_selection_model = self.ui.category_view.selectionModel()
        category_selection_model.selectionChanged[QItemSelection, QItemSelection].connect(self.__update_data_selected_categories)

        # set model for product view
        self.__product_mdl = QStandardItemModel()
        self.ui.product_view.setModel(self.__product_mdl)
        self.ui.product_view.setSelectionMode(QAbstractItemView.SingleSelection)

        # populate product view model
        product_data_lst = self.__model.products_from_categories([])        
        self.__update_view_product('product', product_data_lst)
        product_selection_model = self.ui.product_view.selectionModel()
        product_selection_model.selectionChanged[QItemSelection, QItemSelection].connect(self.__update_data_selected_product)

        # set model for alternative product view
        self.alternative_mdl = QStandardItemModel()
        self.ui.alternative_view.setModel(self.alternative_mdl)
        self.ui.alternative_view.setSelectionMode(QAbstractItemView.SingleSelection)

        altern_category_cbox = self.ui.altern_category_cbox
        altern_category_cbox.currentIndexChanged[int].connect(self.__update_data_alternative_product)
        
    def __create_widgets(self):

        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def __update_view_category(self):

        # get category data
        category_data_lst = self.__model.categories()
        
        # view
        self.ui.category_view.setSortingEnabled(False)
        self.category_stdmodel.clear()
        self.category_stdmodel.setHorizontalHeaderLabels(['Category'])

        for data_dct in category_data_lst:

            item = QStandardItem( data_dct['name'] )
            item.setData(data_dct['id'])
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.category_stdmodel.appendRow(item)

        self.ui.category_view.setSortingEnabled(True)

    def __update_view_product(self, model_type, product_data_lst):

        # view
        is_checked = True

        if model_type == 'product':
            model = self.__product_mdl
        elif model_type == 'alternative':
            model = self.alternative_mdl
        else:
            is_checked = False

        if is_checked:

            model.clear()

            header_lst = ['Brand', 'Name', 'code', 'Store', 'Nutri-Score', 'Nova score', 'UK Nutri-Score', 'Edited']
            model.setHorizontalHeaderLabels(header_lst)


            row_idx = 0
            for data_dct in product_data_lst:

                item_lst = []

                item = QStandardItem( data_dct['brands'] )
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                item_lst.append(item)

                item = QStandardItem( data_dct['name'] )
                item.setData(data_dct['product_code'])
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                item_lst.append(item)

                item = QStandardItem( data_dct['product_code'] )
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                item_lst.append(item)

                item = QStandardItem( ''.join(data_dct['stores']) )
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                item_lst.append(item)

                item = QStandardItem( data_dct['nutrition_grades'] )
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                item_lst.append(item)

                nova = data_dct['nova_group']
                # print(nova)
                if int(nova) > 0:
                    s = str(nova)
                else:
                    s = ""
                item = QStandardItem( s )
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                item_lst.append(item)

                # nutrition_score = data_dct['nutrition_score']
                # if nutrition_score >= 0:
                #     s = str(nutrition_score)
                # else:
                #     s = ""
                # item = QStandardItem( s )
                # item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                # item_lst.append(item)

                # time = data_dct['last_modified_t']
                # if time >= 0:
                #     s = str(QDateTime().setTime_t(time))
                # else:
                #     s = ""
                # item = QStandardItem( s )
                # item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                # item_lst.append(item)

                model.appendRow(item_lst)
                # model.setItem(row_idx, item)
                row_idx = row_idx + 1

    def __update_data_selected_categories(self, selected_item, deselected_item):
        """ Get the list of selected category items, then get item data back and update the list of selected category id. """

        # deselected items
        for model_index in deselected_item.indexes():

            category_id = model_index.data(Qt.UserRole+1)
            
            if category_id in self.__selected_category_lst:
                self.__selected_category_lst.remove(category_id)

        # new selected items
        for model_index in selected_item.indexes():

            category_id = model_index.data(Qt.UserRole+1)
            
            if category_id not in self.__selected_category_lst:
                self.__selected_category_lst.append(category_id)
        
        self.__lg.debug('\t  - {} Selected categories: {}'.format(len(self.__selected_category_lst), self.__selected_category_lst))

        product_data_lst = self.__model.products_from_categories(self.__selected_category_lst)
        self.__update_view_product('product', product_data_lst)

    def __update_data_selected_product(self, selected_item, deselected_item):

        product_code = selected_item.indexes()[1].data(Qt.UserRole+1)
        print('selected product', selected_item.indexes()[1].data(), product_code )

        product_data_dct = self.__model.products([product_code])
        
        category_lst = self.__model.category_data(product_data_dct[product_code]['categories_hierarchy'])

        altern_category_cbox = self.ui.altern_category_cbox

        altern_category_cbox.blockSignals(True)
        altern_category_cbox.clear()

        for category_dct in category_lst:

            # altern_category_cbox.insertItem(-1, category_data['name'], category_id)
            altern_category_cbox.addItem(category_dct['name'], category_dct['id'])

        altern_category_cbox.blockSignals(False)
        cnt = altern_category_cbox.count()
        if cnt > 0:
            altern_category_cbox.setCurrentIndex(cnt-1)

    def __update_data_alternative_product(self, category_index):

        product_code = self.ui.product_view.selectionModel().selectedIndexes()[1].data(Qt.UserRole+1)
        
        category_id = self.ui.altern_category_cbox.itemData(category_index)
        # category_id = self.ui.altern_category_cbox.currentData()

        product_data_lst = self.__model.alternative_products(product_code, category_id)
        self.__update_view_product('alternative', product_data_lst)


    def print_test(self, check):
        ##        print(newAct.iconText(), newAct.text())
        #        print(self.ui_project_command._action_new.text())
        #
        #        text = QInputDialog.getText(self, "QInputDialog::getText()",
        #                                         "User name:")
        ##                                         QLineEdit::Normal,
        ##                                         QDir::home().dirName(), &ok);
        ##        if (ok && !text.isEmpty())
        ##            textLabel->setText(text);
        #        print(text)
        pass

#        self.ui.project_list_combo.addItem("None")
#
#        self.ui.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
#        self.ui.table_view.setShowGrid(False)
#
#        # file command
#        icon_lst = [ZView_Command.ICON_TYPE_NEW,
#                    ZView_Command.ICON_TYPE_COPY,
#                    ZView_Command.ICON_TYPE_EDIT,
#                    ZView_Command.ICON_TYPE_MULTI_EDIT,
#                    ZView_Command.ICON_TYPE_CHECK,
#                    ZView_Command.ICON_TYPE_VALID,
#                    ZView_Command.ICON_TYPE_TEMPLATE,
#                    ZView_Command.ICON_TYPE_DELETE,
#                    ZView_Command.ICON_TYPE_SAVE,
#                    ZView_Command.ICON_TYPE_SAVE_AS
#                    ]
#
#        # project
#        icon_lst = [ZView_Command.ICON_TYPE_NEW,
#                    ZView_Command.ICON_TYPE_EDIT,
#                    ZView_Command.ICON_TYPE_DELETE,
##                    ZView_Command.ICON_TYPE_SAVE,
#                    ]
#        self.ui_project_command = ZView_Command(icon_lst)
#        self.ui.project_edit_grpbx.layout().insertWidget(0, self.ui_project_command)
#
#
#
#        # credit command
#        icon_lst = [ZView_Command.ICON_TYPE_NEW, ZView_Command.ICON_TYPE_COPY,
#                    ZView_Command.ICON_TYPE_EDIT,
#                    ZView_Command.ICON_TYPE_MULTI_EDIT,
#                    ZView_Command.ICON_TYPE_DELETE
#                    ]
#        self.ui_credit_command = ZView_Command(icon_lst)
#        self.ui.credit_grpbx.layout().insertWidget(0, self.ui_credit_command)
#
#
#        self.ui_event = ZEventView()
#        self.ui_event.ui.entity_dest_cb.addItem('Project', ZEvent.ENTITY_PROJECT)
#        self.ui_event.ui.entity_dest_cb.addItem('Bank', ZEvent.ENTITY_BANK)
#
#        self.ui_event.ui.stock_cb.addItem('Loan', ZEvent_Owner.RESSOURCE_SRC_LOAN)
#        self.ui_event.ui.stock_cb.addItem('Personal', ZEvent_Owner.RESSOURCE_SRC_PERSONAL)
#
#        self.ui_event.accepted.connect(self.__set_event)

#    def combo_current_index_changed(self, i_index):
#
##        print('Project ComboBox Current index changed from', self.__currentProjectIndex, 'to', i_index)
#        self.__model.load_project(i_index)
#
#    def __new_project(self, check):
#
#        label, ok = QInputDialog.getText(self, "Add new project",
#                                         "Project label")
#        if ok and label:
#            self.ui.project_list_combo.addItem(label)
#
#            self.__model.add_project(label)
#
#    def __edit_project(self, check):
#
#        label_cur = self.ui.project_list_combo.currentText()
#
#
#        label, ok = QInputDialog.getText(self, "Edit project name",
#                                         'Project label', text=label_cur)
#        if ok and label and label != label_cur:
#
#            self.ui.project_list_combo.setItemText(
#                    self.__model.current_project_id, label)
#
#            self.__model.set_project_label(label)
#
#    def __delete_project(self, check):
#
#        index = self.ui.project_list_combo.currentIndex()
#
#        # if the last item add dummy project
#        if self.ui.project_list_combo.count() == 1:
#
#            label = 'Demo'
#            self.ui.project_list_combo.addItem(label)
#            self.__model.add_project(label)
#
#        # delete item
#        self.ui.project_list_combo.removeItem(index)
#
#        self.__model.delete_project(index)
#
##    def __load_project(self, i_index=-1):
##
##        self.__model.load_project(i_index)
##
##        self.ui.inCapital_spin.setValue(project['capital'])
##
##        period_mth = project['period_mth']
##        self.ui.inPeriod_mth_spin.setValue(period_mth)
##
##        period_year, period_day = ZCredit.ConvertNMonth(period_mth)
##        self.ui.inPeriod_yr_dspin.setValue(period_year)
#
#    def set_period_yr(self, val):
#
##        print('set_period_year')
#
#        self.__model.set_period_mth(ZCredit.n_year_to_n_month(val))
#
#        self.ui.inPeriod_mth_spin.blockSignals(True)
#        self.ui.inPeriod_mth_spin.setValue(self.__model.credit.period_mth)
#        self.ui.inPeriod_mth_spin.blockSignals(False)
#
##        self.__update_output_parameters()
#
#    def set_period_mth(self, val):
#
##        print('set_period_mth')
#        self.__model.set_period_mth(val)
#
#        self.ui.inPeriod_yr_dspin.blockSignals(True)
#        n_year = ZCredit.n_month_to_n_year(self.__model.credit.period_mth)
#        self.ui.inPeriod_yr_dspin.setValue(n_year)
#        self.ui.inPeriod_yr_dspin.blockSignals(False)
##        self.__update_output_parameters()
#
##    def set_payment_per_month(self, val):
##
##        self.__model.credit.payment_per_month = val
##        self.__update_output_parameters()
#
#    def set_capital_from_output(self, checked):
#
#        self.ui.inCapital_spin.setValue(self.ui.outCapital_spin.value())
#
#    def set_rate_from_output(self, checked):
#
#        self.ui.inYearlyRate_dspin.setValue(self.ui.outYearlyRate_dspin.value())
#
#    def set_period_from_output(self, checked):
#
#        self.ui.inPeriod_mth_spin.setValue(self.ui.outPeriod_mth_spin.value())
#
#    def set_payment_from_output(self, checked):
#
#        self.ui.inMonthlyPayment_dspin.setValue(self.ui.outMonthlyPayment_dspin.value())
#
##    def new_event(self, checked):
##
##        pass
#
#    def __create_event(self, checked):
#
#        self.ui_event._is_new_event = True
#
#        # Open dialogue box (ok/cancel)
#        self.__open_event_form()
#
#    def __copy_event(self, checked):
#
#        self.ui_event._is_new_event = True
#
#        # copy event parameters into form:
#        # - get event id.
#        # - get event parameters.
#        # - set form
#
#        self.__open_event_form()
#
#    def __edit_event(self, checked):
#
#        # copy event parameters into form:
#        # - get event id.
#        # - get event parameters.
#        # - set form
#
#        self.ui_event._is_new_event = False
#
#        self.__open_event_form()
#
#    def __remove_event(self, checked):
#
#        # Get selected row
#        row_list = [select.row() for select in self.ui.table_view.selectedIndexes()]
#
#        row_list = list(set(row_list))
#        print('selected row list', row_list)
#
#        # Get event id. list
#        id_list = list()
#        for row in row_list:
#            print('data:', self.ui.table_model.item(row, self.__model._data_frame_label.index('Id.')).data())
##            id_list.append(int(self.ui.table_model.item(row, self.__model._data_frame_label.index('Id.')).text()))
#            id_list.append(self.ui.table_model.item(row, self.__model._data_frame_label.index('Id.')).data())
#
#        self.__model.remove_event(id_list)
#
#    def __open_event_form(self):
#
#        self.ui_event.exec()
#
#
#    def __set_event(self):
#
##        print('set event function')
#
#        event_dct = dict()
#
#        # Get parameters:
#
#        # - Date / Entity_type / amount /
#        event_dct['date'] = self.ui_event.ui.dateEdit.dateTime().toPyDateTime()
#        event_dct['entity'] = self.ui_event.ui.entity_cb.currentIndex()
#        event_dct['amount'] = self.ui_event.ui.amount_dspn.value()
#
#        #   - Project: third / product / operation / category
#        event_dct['third'] = self.ui_event.ui.third_cb.currentText()
#        event_dct['product'] = self.ui_event.ui.product_cb.currentText()
#        event_dct['operation'] = self.ui_event.ui.operation_cb.currentText()
#        event_dct['category'] = self.ui_event.ui.category_cb.currentText()
#
#        #   - Owner: stock_src / entity_dest / id_dest
#        event_dct['stock_src'] = self.ui_event.ui.stock_cb.currentData()
#        event_dct['entity_dest'] = self.ui_event.ui.entity_dest_cb.currentData()
#        event_dct['id_dest'] = self.ui_event.ui.transaction_id_cb.currentIndex()
#
#        #   - Bank: credit_src <=> cf. id_dest / transaction type
#        event_dct['credit_src'] = self.ui_event.ui.credit_cb.currentIndex()
#
#        if self.ui_event._is_new_event:
#            # add new event
#            event_dct['id'] = ZEvent.EVENT_ID_DEFAULT
#
#            self.__model.set_event(**event_dct)
#
#        else:
#            # edit event
#            event_dct['id'] = int(self.ui_event.ui.id_lab.text())
#            print('event id.: {}'.format(int(self.ui_event.ui.id_lab.text())))
#
##        self.__update_output_parameters()
#
#    def __select_credit(self):
#
#        items_lst = self.ui.credit_tree_widget.selectedItems()
#
#        for item in items_lst:
#            print('selected item id',
#                  item.data(self.__CREDIT_TREE_DATA_LABEL.index('Id.'),
#                            Qt.DisplayRole))
#
#        print(items_lst)
#        self.__model.select_credit(items_lst[0].data(
#                self.__CREDIT_TREE_DATA_LABEL.index('Id.'), Qt.DisplayRole))
#
#    def update(self, message):
#
#        if message == ZFunding.OBS_MSG_INIT_PROJECT:
#
#            self.__update_credit_tree()
#            self.__update_input_parameters()
#            self.__update_output_parameters()
#            self.__update_event_table_view()
#
#            self.ui.project_list_combo.blockSignals(True)
#            self.ui.project_list_combo.setCurrentIndex(self.__model.current_project_id)
#            self.ui.project_list_combo.blockSignals(False)
#
#        elif message == ZFunding.OBS_MSG_UPDATE_DATA:
#
#            self.__update_output_parameters()
#            self.__update_event_table_view()
#
#        elif message == ZFunding.OBS_MSG_UPDATE_CREDIT:
#
#            self.__update_input_parameters()
#            self.__update_output_parameters()
#            self.__update_credit_tree()
#
#        else:
#            print('/!\ Error : Credit_View class update message unknown:', message)
#
#
#    def __update_credit_tree(self):
#
#        tree = self.ui.credit_tree_widget
#        tree.blockSignals(True)
#
#        tree.clear()
#
#        self.__set_credit_tree(tree.invisibleRootItem(), self.__model.root_credit)
#
#        tree.setHeaderLabels(self.__CREDIT_TREE_DATA_LABEL)
#
#        tree.blockSignals(False)
#
#
#    def __set_credit_tree(self, root_item, node):
#
#        item = QTreeWidgetItem(root_item)
#        item.setData(self.__CREDIT_TREE_DATA_LABEL.index('Label'), Qt.DisplayRole, node.label)
#        item.setData(self.__CREDIT_TREE_DATA_LABEL.index('Id.'), Qt.DisplayRole, node._id)
#        item.setData(self.__CREDIT_TREE_DATA_LABEL.index('Capital'), Qt.DisplayRole, node.capital)
#
#        for child in node._child_lst:
#
#            self.__set_credit_tree(item, child)
#
#    def __update_input_parameters(self):
#
#        credit = self.__model.credit
#
#        self.ui.inCapital_spin.blockSignals(True)
#        self.ui.inCapital_spin.setValue(credit.capital)
#        self.ui.inCapital_spin.blockSignals(False)
#
#        period_mth = credit.period_mth
#        self.ui.inPeriod_mth_spin.blockSignals(True)
#        self.ui.inPeriod_mth_spin.setValue(period_mth)
#        self.ui.inPeriod_mth_spin.blockSignals(False)
#
#        period_year = ZCredit.n_month_to_n_year(period_mth)
#        self.ui.inPeriod_yr_dspin.blockSignals(True)
#        self.ui.inPeriod_yr_dspin.setValue(period_year)
#        self.ui.inPeriod_yr_dspin.blockSignals(False)
#
#        self.ui.inYearlyRate_dspin.blockSignals(True)
#        self.ui.inYearlyRate_dspin.setValue(credit.rate_per_year)
#        self.ui.inYearlyRate_dspin.blockSignals(False)
#
#        self.ui.inMonthlyPayment_dspin.blockSignals(True)
#        self.ui.inMonthlyPayment_dspin.setValue(credit.payment_per_month)
#        self.ui.inMonthlyPayment_dspin.blockSignals(False)
#
#    def __update_output_parameters(self):
#
#        credit = self.__model.credit
#
#        self.ui.outCapital_spin.setValue(credit.estimated_capital())
#        self.ui.outYearlyRate_dspin.setValue(credit.estimated_rate_per_year())
#
#        estimated_period_mth = credit.estimated_period_mth()
#        self.ui.outPeriod_yr_dspin.setValue(ZCredit.n_month_to_n_year(estimated_period_mth))
#        self.ui.outPeriod_mth_spin.setValue(estimated_period_mth)
#
#        self.ui.outMonthlyPayment_dspin.setValue(credit.estimated_payment_per_month())
#
#        cost, cost_rate = self.__model.credit.estimated_total_cost()
#        self.ui.outCost_dspin.setValue( cost )
#        self.ui.outCostRate_dspin.setValue( cost_rate )



# #        label_lst = self.__model._data_frame_label
#         label_lst = ['a','b','c','d','e']
# #        n_rows = data.shape[0]
#         n_rows = 20
#         for row_idx in range(n_rows):

#             for col_idx, label in enumerate(label_lst):

#                 item = QStandardItem( 'str_{}'.format(row_idx+col_idx) )
#                 item.setData(row_idx+col_idx)
#                 item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

#                 item_0 = QStandardItem( 'str_{}'.format((row_idx+col_idx)*10) )
#                 item.appendRow(item_0)
#                 item_1 = QStandardItem( 'str_{}'.format((row_idx+col_idx)*100) )
#                 item_0.appendRow(item_1)
#                 self.category_stdmodel.setItem(row_idx, col_idx, item)


#        for col_idx, label in enumerate(label_lst):
#
#            s = label.replace("P:", "Project\n")
#            s = s.replace("O:", "Owner\n")
#            s = s.replace("B:", "Bank\n")
#            s = s.replace("Cumulative_Loan_Funds", "Cumulative\nLoan_Funds")
#            s = s.replace("Cumulative_Personal_Funds", "Cumulative\nPersonal_Funds")
#            s = s.replace("ative", ".")
#            s = s.replace("onal", ".")
#            s = s.replace("dest", "dest.")
#            s = s.replace("_", " ")
#
#            self.ui.table_model.setHeaderData(col_idx, Qt.Horizontal, s)
#
#        self.ui.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
##        self.ui.table_view.hideColumn(label_lst.index('Id.'))
#        self.ui.table_view.hideColumn(label_lst.index('Entity'))

#        print('please print scheduler')
#        data = credit.estimated_schedule()

##class ZTest(QWidget):
##
##    def __init__(self, parent=None):
##
##        super(ZTest, self).__init__(parent)
##
##        self.ui = Ui_Form()
##        self.ui.setupUi(self)


if __name__ == "__main__":

    # add 'model' package
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'z_model'))
    from fact import ZFact as ZModel


    app = QApplication(sys.argv)


    model = ZModel()

    ui = ZOpynFacts_View(model)
    ui.show()

#    ui = QDialog()
#    f = Ui_Form()
#    f.setupUi(ui)
#    ui.show()

    sys.exit( app.exec_() )
