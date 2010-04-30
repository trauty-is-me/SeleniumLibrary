#  Copyright 2008-2009 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

class Table(object):

    def _get_locator(self, table_locator):
        if table_locator.startswith("css="):
            return table_locator
        else:
            return "css=table#%s" % (table_locator)
                    
    def table_should_contain(self, table_locator, expected_content):
        """Asserts that the `expected content` can be found somewhere in the table. 
        
        To understand how tables are identified, please take a look at the `introduction`. 
        """
        locator = self._get_locator(table_locator) + ":contains('%s')" % (expected_content)
        message = "Table identified by '%s' should have contained text '%s'." % (table_locator, expected_content)
        self._page_should_contain_element(locator, 'element', message)

    def table_header_should_contain(self, table_locator, expected_content):
        """
        Asserts that the table header, i.e. any <th>...</th> element, contains the `expected_content`.
        
        To understand how tables are identified, please take a look at the `introduction`. 
        """
        locator = self._get_locator(table_locator) + " th:contains('%s')" % (expected_content)
        message = "Header in table identified by '%s' should have contained text '%s'." % (table_locator, expected_content)
        self._page_should_contain_element(locator, 'element', message)

    def table_footer_should_contain(self, table_locator, expected_content):
        """Asserts that the table footer, i.e. any td-element inside a <tfoor>...<tfoot> element, 
        contains the `expected_content`.
        
        To understand how tables are identified, please take a look at the `introduction`. 
        """
        locator = self._get_locator(table_locator) + " tfoot td:contains('%s')" % (expected_content)
        message = "Footer in table identified by '%s' should have contained text '%s'." % (table_locator, expected_content)
        self._page_should_contain_element(locator, 'element', message)

    def table_row_should_contain(self, table_locator, row, expected_content):
        """Asserts that a specific table row contains the `expected_content`. The uppermost row is row number 1. 
        For tables that are structured with thead, tbody and tfoot, only the tbody section is searched. Please use 
        `Table Header Should Contain` or `Table Footer Should Contain` for tests agains the header or footer content.

        If the table contains cells that span multiple rows, a match only occurs for the uppermost row of those merged cells.
        
        To understand how tables are identified, please take a look at the `introduction`. 
        """
        locator = self._get_locator(table_locator) + " tr:nth-child(%s):contains('%s')" % (row, expected_content)
        message = "Row #%s in table identified by '%s' should have contained text '%s'." % (row, table_locator, expected_content)
        self._page_should_contain_element(locator, 'element', message)

    def table_column_should_contain(self, table_locator, col, expected_content):
        """Asserts that a specific column contains the `expected_content`. The first leftmost column is column number 1.
        
        If the table contains cells that span multiple columns, those merged cells count as a single column. For example both tests
        below work, if in one row columns A and B are merged with colspan="2", and the logical third column contains "C". 
        
        Example:
        | Table Column Should Contain | tableId | 3 | C |
        | Table Column Should Contain | tableId | 2 | C |
        
        To understand how tables are identified, please take a look at the `introduction`. 
        """
        locator = self._get_locator(table_locator) + " tr td:nth-child(%s):contains('%s')" % (col, expected_content)
        message = "Column #%s in table identified by '%s' should have contained text '%s'." % (col, table_locator, expected_content)
        try: 
            self._page_should_contain_element(locator, 'element', message)
        except AssertionError, err:
            if 'should have contained text' not in self._get_error_message(err):
                raise
            locator = self._get_locator(table_locator) + " tr th:nth-child(%s):contains('%s')" % (col, expected_content)
            self._page_should_contain_element(locator, 'element', message)
    
    def get_table_cell(self, table_locator, row, column):
        """Reads the content from a table cell. Row and Column number are starting from 1. 
        
        To understand how tables are identified, please take a look at the `introduction`. 
        """
        return self._selenium.get_table("%s.%d.%d" % (self._get_locator(table_locator), int(row) - 1, int(column) - 1))
        
    def table_cell_should_contain(self, table_locator, row, column, expected_content):
        """Asserts that a certain cell in a table contains the `expected content'. Row and Column number are starting from 1. 
        
        To understand how tables are identified, please take a look at the `introduction`. 
        """
        message = "Cell in table '%s' in row #%s and column #%s should have contained text '%s'." % (table_locator, row, column, expected_content)
        try:
            content = self.get_table_cell(table_locator, row, column)
        except Exception, err:
            self._info(self._get_error_message(err))
            raise AssertionError(message)
        self._info("Cell contains %s." % (content))
        if not expected_content in content:
            raise AssertionError(message)