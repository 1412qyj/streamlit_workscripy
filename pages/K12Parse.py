import os , re

import streamlit as st
import pandas as pd
import plotly.express as px

def is_hex_str(data):
    try:
        int(data, 16)
        return True
    except:
        return False

def is_number_or_decimal(string):
    # 使用正则表达式匹配数字或小数的模式
    pattern = r'^[-+]?[0-9]*\.?[0-9]+$'
    return re.match(pattern, string) is not None

def mul_dataframe(df: pd.DataFrame, column, factor):
    if not pd.api.types.is_numeric_dtype(df[column]):
        st.error(f'{column} 不支持 Mul 操作')

    df[column] = df[column] * factor

def hex2dec_dataframe(df: pd.DataFrame, column):
    if df[column].dtype != object or not is_hex_str(df[column][0]):
        st.error(f'{column} 不支持 Hex2Dec 操作')
        return 
    
    df[column] = df[column].apply(lambda x: int(x, 16))
    
def diff_dataframe(df: pd.DataFrame, column):
    if not pd.api.types.is_numeric_dtype(df[column]):
        st.error(f'{column} 不支持 Diff 操作')

    df[column] = df[column].diff()


def plot_dataframe(df: pd.DataFrame, column):
    if not pd.api.types.is_numeric_dtype(df[column]):
        st.error(f'{column} 不支持 Plot 操作')
    
    st.line_chart(df[column])


st.title('K12Parse')

new_file = st.file_uploader('选择文件 (K12.txt) or (csv)', type=['csv']) # TODO: txt

if 'target_file' not in st.session_state:
    st.session_state.target_file = None

if new_file:
    if  new_file != st.session_state.target_file:
        # csv文件直接解析
        if os.path.splitext(new_file.name)[1] == '.csv':
            df = pd.read_csv(new_file)
            st.session_state.table_data = df
            st.session_state.columns = df.columns
            st.session_state.target_file = new_file
        else:
            st.info('暂不支持 txt 格式, 请等待升级 ')
    
    column_select = st.sidebar.selectbox('当前操作的列名', st.session_state.columns)
    options = st.sidebar.selectbox('当前的操作', ('Hex2Dec','Mul','Plot', 'Diff'))
    mulfactor = ''
    if options == 'Mul':
        mulfactor = st.sidebar.text_input('请输入 Mul 系数')

    exec_options = st.sidebar.button('执行操作')

    if exec_options:
        if options == 'Mul':
            if is_number_or_decimal(mulfactor):
                mul_dataframe(st.session_state.table_data, column_select, float(mulfactor))
            else:
                st.sidebar.error('请输入 数字')
            
        elif options == 'Hex2Dec':
            hex2dec_dataframe(st.session_state.table_data, column_select)
        elif options == 'Diff':
            diff_dataframe(st.session_state.table_data, column_select)
        elif options == 'Plot':
            plot_dataframe(st.session_state.table_data, column_select)
        else:
            pass
    st.write(st.session_state.table_data.head(10))