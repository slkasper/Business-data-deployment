from datetime import datetime
import streamlit as st


def rename_key(title:str)->str:
    new_title = "_".join(title.split(' ')).lower()
    return new_title


def selection_box_widget(selectbox_title:str, selectbox_options:list, initial_selection:int=0):
    '''
    Pass in selection box title as string and list of options for selection.
    If you want to use the title for notes, be sure to call a st.header("Title")
      for nicer title display.
    `initial_selection` calls the index location of the selectbox_options list that you want
    for the initial st.session_state. Default is the first entry (0).
    '''
    selection_box = st.selectbox(
        selectbox_title,
        selectbox_options,
        index=initial_selection,
        key=rename_key(selectbox_title)
        )
    return selection_box

#not used
def slider_widget(slider_title:str, slider_options:list):
    '''
    Pass in slider title as string and the list of options for the slider. 
    If you need to order the list, be sure to do that formatting first.
    This function assumes an ordered range
    '''
    slider = st.select_slider(
        slider_title, 
        options=slider_options,  
        value= (slider_options[0], slider_options[-1]),
        key=rename_key(slider_title)
        )
    return slider

def multiselect_widget(multiselect_title:str, multiselect_options:list):
    '''
    Pass in selection box title as string and list of options for selection.
    If you want to use the title for notes, be sure to call a st.header("Title")
      for nicer title display.
    Inital selection is controled by checkbox_widget_all and multi_select_all. No options 
        show in the box, but the checkbox makes sure they are all on in the background initially
        avoiding ugly, unusable selection box filled with all options.
    '''
    multiselect = st.multiselect(
        multiselect_title,
        multiselect_options,
        key=multiselect_title
        )
    return multiselect   

#not used
def checkbox_widget_all(name):
    '''Helper widget to default multiselct all on, in case of empty filter values'''
    all_options = st.checkbox(f"Select all {name}", True)
    return all_options

#not used
def multiselect_select_all(all_options:bool, session_selection:list, full_list:list):   
    if all_options:
        #if all_on for multiselect checkbox = true, set session value to full list of options
        session_selection = full_list
        return session_selection
    elif len(session_selection) == 0:
        # if session value is empty, output warning - filter set to all TRUE in data_processing.py
        return st.markdown('''**:red[Selection returned no results. Filter ignored]**''')
    
def build_datetime_name():
    now = datetime.now()
    txt_datetime = now.strftime("%m-%d-%Y-%H:%M")
    return txt_datetime
