import json
import os
import tkinter
from tkinter import ttk, filedialog, StringVar, IntVar

workflow_path = ''
inputs_path = ''
options_path = ''
initial_dir = '~'


def select_workflow_file():
    global workflow_path, initial_dir
    file_types = (('workflow files', '*.wdl'),
                  ('All files', '*.*'))
    workflow_path = filedialog.askopenfilename(title='Open a file',
                                               initialdir=initial_dir,
                                               filetypes=file_types)
    initial_dir = os.path.join(*workflow_path.split(os.sep)[:1])


def select_inputs_file():
    global inputs_path, initial_dir
    file_types = (('input file', '*.json'),
                  ('All files', '*.*'))
    inputs_path = filedialog.askopenfilename(title='Open a file',
                                             initialdir=initial_dir,
                                             filetypes=file_types)
    initial_dir = os.path.join(*inputs_path.split(os.sep)[:1])


def select_options_file():
    global options_path, initial_dir
    file_types = (('options file', '*.json'),
                  ('All files', '*.*'))
    options_path = filedialog.askopenfilename(title='Open a file',
                                              initialdir=initial_dir,
                                              filetypes=file_types)
    initial_dir = os.path.join(*options_path.split(os.sep)[:1])


def submit_function():
    global requester, workflow_path, inputs_path, options_path, vexecution_id
    execution_id = requester.submit_workflow(workflow_path, inputs_path, options_path)
    vexecution_id.set(execution_id)


def request_API():
    global vexecution_id, requester
    txt_output.delete('1.0', tkinter.END)
    option = sel_option.get()
    if option == 'status':
        output = requester.get_status(vexecution_id.get())
    elif option == 'logs':
        output = requester.get_log(vexecution_id.get())
    elif option == 'outputs':
        output = requester.get_outputs(vexecution_id.get())
    elif option == 'metadata':
        output = requester.get_metadata(vexecution_id.get())
    elif option == 'abort':
        output = requester.abort_execution(vexecution_id.get())
    else:
        output = "Unrecognized option "+option

    if output.startswith('{') and vpretty.get() == 1:
        json_obj = json.loads(output)
        output = json.dumps(json_obj, indent=2)
    txt_output.insert('end', output)


if __name__ == '__main__':
    from modules.cromwell_request import CromwellRequester

    requester = CromwellRequester()

    main_screen = tkinter.Tk()
    main_screen.title('Cromwell requester')

    vexecution_id = StringVar()
    vexecution_id.set('')

    voutput = StringVar()
    voutput.set('')

    vpretty = IntVar()

    # Section title
    lbl_title_submit = tkinter.Label(text='Submit new workflow to Cromwell', )
    # Workflow Selection
    lbl_lworkflow = tkinter.Label(text='Workflow file*:')
    btn_load_workflow = tkinter.Button(text='Select .wdl file', command=select_workflow_file)
    # Inputs selection
    lbl_linputs = tkinter.Label(text='Inputs file:')
    btn_load_inputs = tkinter.Button(text='Select .json file', command=select_inputs_file)
    # Options selection
    lbl_loptions = tkinter.Label(text='Options file:')
    btn_load_options = tkinter.Button(text='Select .json file', command=select_options_file)
    # Submit workflow button
    btn_submit = tkinter.Button(text='Submit to Cromwell', bg='blue', command=submit_function)

    # Separator
    separator1 = ttk.Separator(orient='horizontal', class_=ttk.Separator, takefocus=1, cursor='plus')
    # Execution id field
    lbl_id = tkinter.Label(text='Execution ID:')
    lbl_execution_id = tkinter.Entry(textvariable=vexecution_id)
    # Separator
    separator2 = ttk.Separator(orient='horizontal', class_=ttk.Separator, takefocus=1, cursor='plus')

    # Section title
    lbl_title_options = tkinter.Label(text='API options', justify='left')
    # API request section
    lbl_option = tkinter.Label(text='Option')
    sel_option = ttk.Combobox(values=['status', 'logs', 'outputs', 'metadata', 'abort'])
    chk_pretty = ttk.Checkbutton(text='Pretty print', variable=vpretty)
    btn_exec = tkinter.Button(text='Request to API', command=request_API)
    # Output text box
    txt_output = tkinter.Text()

    # Displaying-----------------------------------

    # Section title
    lbl_title_submit.grid(row=0, column=0, columnspan=2)
    # Workflow Selection
    lbl_lworkflow.grid(row=1, column=0)
    btn_load_workflow.grid(row=1, column=1)
    # Inputs selection
    lbl_linputs.grid(row=2, column=0)
    btn_load_inputs.grid(row=2, column=1)
    # Options selection
    lbl_loptions.grid(row=3, column=0)
    btn_load_options.grid(row=3, column=1)
    # Submit workflow button
    btn_submit.grid(row=4, column=1, sticky='e')

    # Separator
    separator1.grid(row=5, column=0, ipadx=200, pady=10, columnspan=2)
    # Execution ID field
    lbl_id.grid(row=6, column=0)
    lbl_execution_id.grid(row=6, column=1)
    # Separator
    separator2.grid(row=7, column=0, ipadx=200, pady=10, columnspan=2)

    # API requests title
    lbl_title_options.grid(row=8, column=0, columnspan=2)
    lbl_option.grid(row=9, column=0)
    sel_option.grid(row=9, column=1)
    sel_option.current(0)
    chk_pretty.grid(row=10, column=0)
    btn_exec.grid(row=10, column=1, pady=10, sticky='e')

    # API output textbox
    txt_output.grid(row=0, column=2, rowspan=11)

    main_screen.mainloop()
