import remi.gui as gui
from remi import App

from bug_finding.utils.graph_util import GraphUtil


class MyApp(App):
    """
    https://buildmedia.readthedocs.org/media/pdf/remi/latest/remi.pdf
    """

    def __init__(self, *args):
        super(MyApp, self).__init__(*args)
        self.input = None
        self.clusters = None

    def main(self):
        self.dropDown_item1 = "Element"
        self.dropDown_item2 = "Cosine Similarity"

        container = gui.VBox(width=1500, height=1000)
        self.lbl = gui.Label('Hello, BugKG!')
        self.bt = gui.Button('Search Clusters')
        # self.bt2 = gui.Button('Search Clusters by Cos')
        self.searchbox = gui.TextInput(hint="Please input here...", width=200, height=30)

        self.dropDown = gui.DropDown.new_from_list((self.dropDown_item1, self.dropDown_item2),
                                                   width=200, height=20, margin='10px')
        # self.dropDown.onchange.do(self.drop_down_changed)
        # self.dropDown.select_by_value('DropDownItem 0')

        # self.bt2.onclick.do(self.on_button_pressed, "Name", "Surname")

        # items = ('Danny Young','Christine Holand','Lars Gordon','Roberto Robitaille')
        # self.listView = gui.ListView.new_from_list(items, width=300, height=120, margin='10px')
        # self.listView.onselection.do(self.list_view_on_selected)
        self.table = gui.Table(width=300, height=200, margin='10px')
        self.table.on_table_row_click.do(self.on_table_row_click)
        self.tree = gui.TreeView(width='100%', height=300)
        # setting the listener for the onclick event of the buttons
        self.bt.onclick.do(self.on_button_pressed)

        # appending a widget to another
        container.append(self.lbl)
        container.append(self.searchbox)
        container.append(self.dropDown)
        container.append(self.bt)
        # container.append(self.bt2)
        # container.append(self.listView)
        container.append(self.table)
        container.append(self.tree)

        # returning the root widget
        return container

    # listener function
    def on_button_pressed(self, widget):
        element = self.searchbox.get_value()
        cluster_list = None
        self.input = element
        if self.dropDown.get_value() == self.dropDown_item1:
            cluster_list = GraphUtil.find_clusters_by_element(element)
        elif self.dropDown.get_value() == self.dropDown_item2:
            cluster_list = GraphUtil.find_clusters_by_cos(element)
        self.clusters = cluster_list
        # for tree
        tree_item_list = []
        if cluster_list:
            for cluster in cluster_list:
                tree_item = None
                sub_tree_item_list = []
                for step in cluster:
                    item = gui.TreeItem(f"{step.bug.id}\t{step.id}\t{step.text}")
                    if tree_item:
                        sub_tree_item = item
                        sub_tree_item_list.append(sub_tree_item)
                    else:
                        tree_item = item

                tree_item.append(sub_tree_item_list)
                tree_item_list.append(tree_item)
        self.tree.empty()
        self.tree.append(tree_item_list)
        # for table
        index_cluster_list = [('ID', 'Cluster')]
        if cluster_list:
            for cluster in cluster_list:
                # tree_item = None
                # sub_tree_item_list = []
                for step in cluster:
                    index_cluster_list.append((str(step.cluster_index), step.text))
                    break

        self.table.empty()
        self.table.append_from_list(index_cluster_list)

        # self.lbl.set_text(text)
        # widget.set_text(text)

    # def drop_down_changed(self, widget, value):
    #     self.lbl.set_text('New Combo value: ' + value)

    # def list_view_on_selected(self, widget, selected_item_key):
    #     """ The selection event of the listView, returns a key of the clicked event.
    #         You can retrieve the item rapidly
    #     """
    #     self.lbl.set_text('List selection: ' + self.listView.children[selected_item_key].get_text())

    def on_table_row_click(self, table, row, item):
        self.dialog = gui.GenericDialog(title=item.get_text(), message='Click Ok to transfer content to main page',
                                        width=1500, height=1000)
        # width='500px')

        # verticalContainer = self.dialog.container(width=1500, margin='0px auto',
        #                                   style={'display': 'block', 'overflow': 'hidden'})
        #
        # verticalContainer = self.dialog.container
        # verticalContainer.set_layout_orientation(gui.Container.LAYOUT_VERTICAL)
        horizontalContainer = self.dialog.container
        horizontalContainer.set_layout_orientation(gui.Container.LAYOUT_HORIZONTAL)
        # subContainerLeft = self.dialog.container
        # subContainerRight = self.dialog.container
        #
        # subContainerLeft = gui.Container(width=320,
        #                                  style={'display': 'block', 'overflow': 'auto', 'text-align': 'center'})
        # subContainerMiddle = gui.Container(width=320,
        #                                  style={'display': 'block', 'overflow': 'auto', 'text-align': 'center'})
        # subContainerRight = gui.Container(width=320,
        #                                  style={'display': 'block', 'overflow': 'auto', 'text-align': 'center'})
        #
        #
        # verticalContainer.append([horizontalContainer])
        # horizontalContainer.append([subContainerLeft, subContainerMiddle, subContainerRight])

        # print(row.children)
        # print(row.children['0'].get_text())
        # print(row.children['1'].get_text())
        # print(type(row.children))
        # for table
        cluster_index = int(row.children['0'].get_text())
        cluster = GraphUtil.INDEX_CLUSTER_DICT[cluster_index]
        bugid_stepid_step_list = [('BugID', 'No. Step', 'Step')]
        bugid_stepid_expected_actual_result_list = [('BugID', 'No. Step', 'Expected Result', 'Actual Result')]
        if cluster:
            for step in cluster:
                bugid_stepid_step_list.append((str(step.bug.id), str(step.id), step.text))
                if step.next_step is None:
                    if step.bug.description.expected_results or step.bug.description.actual_results:
                        bugid_stepid_expected_actual_result_list.append((str(step.bug.id), str(step.id),
                                                                         step.bug.description.expected_results,
                                                                         step.bug.description.actual_results))

        self.dtable = gui.Table.new_from_list(bugid_stepid_step_list, width=500, height=200, margin='10px')
        # values = ('Danny Young', 'Christine Holand', 'Lars Gordon', 'Roberto Robitaille')
        # self.dlistView = gui.ListView.new_from_list(values, width=200, height=120)
        # self.dialog.add_field_with_label('dtable', 'Step', self.dtable)

        self.dtable_result = gui.Table.new_from_list(bugid_stepid_expected_actual_result_list, width=500, height=200,
                                                     margin='10px')
        # values = ('Danny Young', 'Christine Holand', 'Lars Gordon', 'Roberto Robitaille')
        # self.dlistView = gui.ListView.new_from_list(values, width=200, height=120)
        # self.dialog.add_field_with_label('dtable_result', 'Step Result', self.dtable_result)

        # subContainerLeft.append([self.dtable])
        # subContainerRight.append([self.dtable_result])

        horizontalContainer.append([self.dtable, self.dtable_result])
        self.dialog.append(horizontalContainer)
        # subContainerLeft.append([])
        # subContainerMiddle.append([self.dtable, self.dtable_result])
        # subContainerRight.append([])

        self.dialog.show(self)

    # def on_tree_item_click(self, step):
    #
    #     self.link = gui.Link(f"https://bugzilla.mozilla.org/show_bug.cgi?id={step.bug.id}", f"Bug {step.bug.id}",
    #                          width=200, height=30, margin='10px')
