from pathlib import Path
from bug_finding.types.element import Element
from bug_finding.utils.file_util import FileUtil
from config import DATA_DIR

if __name__ == "__main__":
    """
    1. get elements from ftl files
    2. get categories of elements from html files (remove elements: a. include both '<' and '>' 
                                                                    b. in category 'Others' )
    3. for elements (category is None), get categories of elements from data-l10n-id
                                                  (remove elements: a. include both '<' and '>' 
                                                                    b. in category 'Others' )
    """
    ftl_file_directory = Path(DATA_DIR, "ftl_files")
    html_file_directory = Path(DATA_DIR, "html_files")

    category_element_dict = Element.get_category_element_dict(ftl_file_directory, html_file_directory)

    for category in category_element_dict.keys():
        # print(type(element_id))
        # print(type(element_id_tag_dict[element_id]))
        print(f"{category}: {category_element_dict[category]}")

    FileUtil.dump_json(Path(DATA_DIR, 'category_element_dict.json'), category_element_dict)
