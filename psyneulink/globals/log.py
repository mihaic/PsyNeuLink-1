# -*- coding: utf-8 -*-
# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
#
# **************************************************  Log **************************************************************

"""

Overview
--------

A Log object is used to record the `value <Component.value>` of PsyNeuLink Components during their "life cycle" (i.e.,
when they are created, validated, and/or executed).  Every Component has a Log object, assigned to its `log
<Component.log>` attribute when the Component is created, that can be used to record its value and/or that of other
Components that belong to it.  These are stored in `entries <Log.entries>` of the Log, that contain a sequential list
of the recorded values, along with the time and context of the recording.  The conditions under which values are
recorded is specified by the `logPref <Component.logPref>` property of a Component.  While these can be set directly,
they are most easily specified using the Log's `set_log_conditions <Log.set_log_conditions>` method, together with its
`loggable_items <Log.loggable_items>` and `logged_items <Log.logged_items>` attributes that identify and track the
items to be logged, respectively. Entries can also be made by the user programmatically, using the `log_values
<Log.log_values>` method. Logging can be useful not only for observing the behavior of a Component in a model, but also
in debugging the model during construction. The entries of a Log can be displayed in a "human readable" table using
its `print_entries <Log.print_entries>` method, and returned in CSV and numpy array formats using its and `nparray
<Log.nparray>` and `csv <Log.csv>`  methods.

.. _Log_Creation:

Creating Logs and Entries
-------------------------

A log object is automatically created for and assigned to a Component's `log <Component.log>` attribute when the
Component is created.  An entry is automatically created and added to the Log's `entries <Log.entries>` attribute
when its `value <Component.value>` or that of a Component that belongs to it is recorded in the Log.

.. _Log_Structure:

Structure
---------

A Log is composed of `entries <Log.entries>`, each of which is a dictionary that maintains a record of the logged
values of a Component.  The key for each entry is a string that is the name of the Component, and its value is a list
of `LogEntry` tuples recording its values.  Each `LogEntry` tuple has three items:
    * *time* -- the `RUN`, `TRIAL` and `TIME_STEP` in which the value of the item was recorded;
    * *context* -- a string indicating the context in which the value was recorded;
    * *value* -- the value of the item.
The time is recorded only if the Component is executed within a `System`;  otherwise, the time field is `None`.

A Log has several attributes and methods that make it easy to manage how and when it values are recorded, and
to access its `entries <Log.entries>`:

    * `loggable_items <Log.loggable_items>` -- a dictionary with the items that can be logged in a Component's `log
      <Component.log>`;  the key for each entry is the name of a Component,  and the value is it current `ContextState`.
    ..
    * `set_log_conditions <Log.set_log_conditions>` -- used to assign the ContextState for one or more Components.
      Components can be specified by their names, a reference to the Component object, in a tuple that specifies the
      `ContextState` to assign to that Component, or in a list with a `ContextState` to be applied to multiple items
      at once.
    ..
    * `log_values <Log.log_values>` -- used to the `value <Component.value>` of one or more Components in the Log
      programmatically ("manually").  Components can be specified by their names or references to the objects.
    ..
    * `logged_items <Log.logged_items>` -- a dictionary with the items that currently have entries in a Component's
      `log <Component.log>`; the key for each entry is the name of a Component, and the value is its current `ContextState`.
    ..
    * `print_entries <Log.print_entries>` -- this prints a formatted list of the `entries <Log.entries>` in the Log.
    ..
    * `nparray <Log.csv>` -- returns a 2d np.array with the `entries <Log.entries>` in the Log.
    ..
    * `csv <Log.csv>` -- returns a CSV-formatted string with the `entries <Log.entries>` in the Log.

.. _Log_Loggable_Items:

Loggable Items
~~~~~~~~~~~~~~

Although every Component is assigned its own Log, that records the `value <Component.value>` of that Component,
the Logs for `Mechanisms <Mechanism>` and `MappingProjections <MappingProjection>` also  provide access to and control
the Logs of their `States <State>`.  Specifically the Logs of these Components contain the following information:

* **Mechanisms**

  * *value* -- the `value <Mechanism_Base.value>` of the Mechanism.
  |
  * *InputStates* -- the `value <InputState.value>` of any `InputState` (listed in the Mechanism's `input_states
    <Mechanism_Base.input_states>` attribute).
  |
  * *ParameterStates* -- the `value <ParameterState.value>` of `ParameterState` (listed in the Mechanism's
    `parameter_states <Mechanism_Base.parameter_states>` attribute);  this includes all of the `user configurable
    <Component_User_Params>` parameters of the Mechanism and its `function <Mechanism_Base.function>`.
  |
  * *OutputStates* -- the `value <OutputState.value>` of any `OutputState` (listed in the Mechanism's `output_states
    <Mechanism_Base.output_states>` attribute).
..
* **Projections**

  * *value* -- the `value <Projection_Base.value>` of the Projection.
  |
  * *matrix* -- the value of the `matrix <MappingProjection.matrix>` parameter (for `MappingProjections
    <MappingProjection>` only).

.. _Log_LogLevels:

ContextStates
~~~~~~~~~~~~~

Configuring a Component to be logged is done using a `ContextState`, that specifies the conditions under which its
`value <Component.value>` should be entered in its Log.  These can be specified in the `set_log_conditions
<Log.set_log_conditions>` method of a Log, or directly by specifying a ContextState for the value a Component's
`logPref  <Compnent.logPref>` item of its `prefs <Component.prefs>` attribute.  The former is easier, and allows
multiple Components to be specied at once, while the latter affords more control over the specification (see
`Preferences`).  ContextStates are treated as binary "flags", and can be combined to permit logging under more than
one condition using bitwise operators on ContextStates.  For convenience, they can also be referred to by their
names, and combined by specifying a list.  For example, all of the following specify that the `value
<Mechanism_Base.value>` of ``my_mech`` be logged both during execution and learning::

    >>> import psyneulink as pnl
    >>> my_mech = pnl.TransferMechanism()
    >>> my_mech.set_log_conditions('value', pnl.ContextState.EXECUTION | pnl.ContextState.LEARNING)
    >>> my_mech.set_log_conditions('value', pnl.ContextState.EXECUTION + pnl.ContextState.LEARNING)
    >>> my_mech.set_log_conditions('value', [pnl.EXECUTION, LEARNING])


.. note::
   Currently, the `VALIDATION` `ContextState` is not implemented.
   COMMENT:
   `VALUE_ASSIGNMENT` AND `FINAL` are also not yet implemented, but these do not appear in the HTML documentation
   COMMENT

.. note::
   Using `ContextState.INITIALIZATION` to log the `value <Component.value>` of a Component during its initialization
   requires that it be assigned in the **prefs** argument of the Component's constructor.  For example::

   COMMENT:
   FIX: THIS EXAMPLE CAN'T CURRENTLY BE EXECUTED AS IT PERMANENTLY SETS THE LogPref FOR ALL TransferMechanism
   COMMENT
    >>> my_mech = pnl.TransferMechanism(
    ...        prefs={pnl.LOG_PREF: pnl.PreferenceEntry(pnl.ContextState.INITIALIZATION, pnl.PreferenceLevel.INSTANCE)})

.. hint::
   `ContextState.TRIAL` logs the `value <Component.value>` of a Component at the end of a `TRIAL`.  To log its
   `value <Component.value>` at the start of a `TRIAL`, use its `log_values <Component.log_values>` method in the
   **call_before_trial** argument of the System's `run <System.run>` method.

.. _Log_Execution:

Execution
---------

The value of a Component is recorded to a Log when the condition assigned to its `logPref <Component.logPref>` is met.
This specified as a `ContextState`.  The default ContextState is `OFF`.

.. _Log_Examples:

Examples
--------

The following example creates a Process with two `TransferMechanisms <TransferMechanism>`, one that projects to
another, and logs the `noise <TransferMechanism.noise>` and *RESULTS* `OutputState` of the first and the
`MappingProjection` from the first to the second::

    # Create a Process with two TransferMechanisms, and get a reference for the Projection created between them:
    >>> my_mech_A = pnl.TransferMechanism(name='mech_A', size=2)
    >>> my_mech_B = pnl.TransferMechanism(name='mech_B', size=3)
    >>> my_process = pnl.Process(pathway=[my_mech_A, my_mech_B])
    >>> my_system = pnl.System(processes=[my_process])
    >>> proj_A_to_B = my_mech_B.path_afferents[0]

    COMMENT:
    FIX: THESE EXAMPLES CAN'T BE EXECUTED AS THEY RETURN DICT ENTRIES IN UNRELIABLE ORDERS
    COMMENT
    # Show the loggable items (and their current ContextStates) of each Mechanism and the Projection between them:
    >> my_mech_A.loggable_items
    {'InputState-0': 'OFF', 'slope': 'OFF', 'RESULTS': 'OFF', 'smoothing_factor': 'OFF', 'intercept': 'OFF', 'noise': 'OFF'}
    >> my_mech_B.loggable_items
    {'InputState-0': 'OFF', 'slope': 'OFF', 'RESULTS': 'OFF', 'intercept': 'OFF', 'noise': 'OFF', 'smoothing_factor': 'OFF'}
    >> proj_A_to_B.loggable_items
    {'value': 'OFF', 'matrix': 'OFF'}

    # Assign the noise parameter and RESULTS OutputState of my_mech_A, and the matrix of the Projection, to be logged
    >>> my_mech_A.set_log_conditions([pnl.NOISE, pnl.RESULTS])
    >>> proj_A_to_B.set_log_conditions(pnl.MATRIX)

Note that since no ContextState was specified, the default (ContextState.EXECUTION) is used. Executing the Process
generates entries in the Logs, that can then be displayed in several ways::

    # Execute the System twice (to generate some values in the logs):
    >>> my_system.execute()
    [array([ 0.,  0.,  0.])]
    >>> my_system.execute()
    [array([ 0.,  0.,  0.])]

    COMMENT:
    FIX: THESE EXAMPLES CAN'T BE EXECUTED AS THEY RETURN DICT ENTRIES IN UNRELIABLE ORDERS
    COMMENT
    # List the items of each Mechanism and the Projection that were actually logged:
    >> my_mech_A.logged_items
    {'RESULTS': 'EXECUTION', 'noise': 'EXECUTION'}
    >> my_mech_B.logged_items
    {}
    >> proj_A_to_B.logged_items
    {'matrix': 'EXECUTION'}

Notice that entries dictionary of the Log for ``my_mech_B`` is empty, since no items were specified to be logged for
it.  The results of the two other logs can be printed to the console using the `print_entries <Log.print_entries>`
method of a Log::

    COMMENT:
    FIX: THIS EXAMPLE CAN'T BE EXECUTED AS IT REQUIRES INSERTION OF "<BLANKLINE>"'S THAT CAN'T BE SUPPRESSED IN HTML
    COMMENT
    # Print the Log for ``my_mech_A``:
    >> my_mech_A.log.print_entries()

    Log for mech_A:

    Logged Item:   Time       Context                                                                   Value

    'RESULTS'      0:0:0     " EXECUTING  System System-0| Mechanism: mech_A [in processes: ['Pro..."   [ 0.  0.]
    'RESULTS'      0:1:0     " EXECUTING  System System-0| Mechanism: mech_A [in processes: ['Pro..."   [ 0.  0.]


    'noise'        0:0:0     " EXECUTING  System System-0| Mechanism: mech_A [in processes: ['Pro..."   [ 0.]
    'noise'        0:1:0     " EXECUTING  System System-0| Mechanism: mech_A [in processes: ['Pro..."   [ 0.]


They can also be exported in numpy array and CSV formats.  The following shows the CSV-formatted output of the Logs
for ``my_mech_A`` and  ``proj_A_to_B``, using different formatting options::

    COMMENT:
    FIX: THESE EXAMPLES CAN'T BE EXECUTED AS THEY RETURN FORMATS ON JENKINS THAT DON'T MATCH THOSE ON LOCAL MACHINE(S)
    COMMENT
    >> print(my_mech_A.log.csv(entries=[pnl.NOISE, pnl.RESULTS], owner_name=False, quotes=None))
    'Run', 'Trial', 'Time_step', 'noise', 'RESULTS'
    0, 0, 0, 0.0, 0.0 0.0
    0, 1, 0, 0.0, 0.0 0.0
    COMMENT:
    <BLANKLINE>
    COMMENT

    # Display the csv formatted entry of Log for ``proj_A_to_B``
    #    with quotes around values and the Projection's name included in the header:
    >> print(proj_A_to_B.log.csv(entries=pnl.MATRIX, owner_name=False, quotes=True))
    'Run', 'Trial', 'Time_step', 'matrix'
    '0', '0', '1', '1.0 1.0 1.0' '1.0 1.0 1.0'
    '0', '1', '1', '1.0 1.0 1.0' '1.0 1.0 1.0'
    COMMENT:
    <BLANKLINE>
    COMMENT

Note that since the `name <Projection.name>` attribute of the Projection was not assigned, its default name is
reported.

The following shows the Log of ``proj_A_to_B`` in numpy array format, with and without header information::

    COMMENT:
    FIX: THESE EXAMPLES CAN'T BE EXECUTED AS THEY RETURN FORMATS ON JENKINS THAT DON'T MATCH THOSE ON LOCAL MACHINE(S)
    COMMENT
    >> proj_A_to_B.log.nparray(entries=[pnl.MATRIX], owner_name=False, header=True)
    [[['Run'] [0] [0]]
     [['Trial'] [0] [1]]
     [['Time_step'] [1] [1]]
     ['matrix' [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]] [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]]]

    >> proj_A_to_B.log.nparray(entries=[pnl.MATRIX], owner_name=False, header=False)
    [[[0] [0]]
     [[0] [1]]
     [[1] [1]]
     [[[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]] [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]]]

COMMENT:
 MY MACHINE:
    >> proj_A_to_B.log.nparray(entries=[pnl.MATRIX], owner_name=False, header=False)
    array([[[0], [1]],
           [[[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]],
            [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]]], dtype=object)

JENKINS:
    >> proj_A_to_B.log.nparray(entries=[pnl.MATRIX], owner_name=False, header=False)
    array([[list([0]), list([1])],
           [list([[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]),
            list([[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]])]], dtype=object)

OR

    print(proj_A_to_B.log.nparray(entries=[pnl.MATRIX], owner_name=False, header=False))
Expected:
    [[[0] [1]]
     [[[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]] [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]]]
Got:
    [[list([0]) list([1])]
     [list([[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]])
      list([[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]])]]
COMMENT


COMMENT:

IMPLEMENTATION NOTE: Name of owner Component is aliases to VALUE in loggable_items and logged_items,
but is the Component's actual name in log_entries

Entries are made to the Log based on the `ContextState` specified in the
`logPref` item of the component's `prefs <Component.prefs>` attribute.

Adding an item to prefs.logPref will validate and add an entry for that attribute to the Log dict

An attribute is logged if:

* it is one `automatically included <LINK>` in logging;
..
* it is included in the *LOG_ENTRIES* entry of a `parameter specification dictionary <ParameterState_Specification>`
  assigned to the **params** argument of the constructor for the Component;
..
* the context of the assignment is above the ContextState specified in the logPref setting of the owner Component

Entry values are added by the setter method for the attribute being logged.

The following entries are automatically included in self.entries for a `Mechanism` object:
    - the value attribute of every State for which the Mechanism is an owner
    [TBI: - value of every projection that sends to those States]
    - the system variables defined in SystemLogEntries (see declaration above)
    - any variables listed in the params[LOG_ENTRIES] of a Mechanism


DEFAULT ContextState FOR ALL COMPONENTS IS *OFF*


Structure
---------

Each entry of `entries <Log.entries>` has:
    + a key that is the name of the attribute being logged
    + a value that is a list of sequentially entered LogEntry tuples since recording of the attribute began
    + each tuple has three items:
        - time (CentralClock): when it was recorded in the run
        - context (str): the context in which it was recorded (i.e., where the attribute value was assigned)
        - value (value): the value assigned to the attribute

The ContextState class (see declaration above) defines six levels of logging:
    + OFF: No logging for attributes of the owner object
    + VALUE_ASSIGNMENT: Log values only when final value assignment has been made during execution
    + EXECUTION: Log values for all assignments during execution (e.g., including aggregation of projections)
    + VALIDATION: Log value assignments during validation as well as execution and initialization
    + ALL_ASSIGNMENTS:  Log all value assignments (e.g., including initialization)
    Note: ContextState is an IntEnum, and thus its values can be used directly in numerical comparisons

Entries can also be added programmatically by:
    - including them in the logPref of a PreferenceSet
    - using the add_entries() method (see below)
    - using the log_entries() method (see below)

The owner.prefs.logPref setting contains a list of entries to actively record
    - when entries are added to an object's logPref list, the log.add_entries() method is called,
        which validates the entries against the object's attributes and SystemLogEntries
    - if entries are removed from the object's logPref list, they still remain in the log dict;
        they can be deleted from the log dict using the remove_log_entries() method
    - data is recorded in an entry using the log_entries() method, which records data to all entries
        in the self.owner.prefs.logPrefs list;  this is generally carried out by the update methods
        of Category classes in the Function hierarchy (e.g., Process, Mechanism and Projection)
        on each cycle of the execution sequence;
    - log_entries() adds entries to the self.owner.prefs.logPrefs list,
        which will record data for those attributes when logging is active;
    - suspend_entries() removes entries from the self.owner.prefs.logPrefs list;
        data will not be recorded for those entries when logging is active

    Notes:
    * A list of viable entries should be defined as the classLogEntries class attribute of a Function subclass
COMMENT


.. _Log_Class_Reference:

Class Reference
---------------

"""
import warnings
import inspect
import typecheck as tc
from collections import namedtuple
# from enum import IntEnum, unique, auto
from enum import IntEnum, unique

import numpy as np

from psyneulink.scheduling.time import TimeScale
from psyneulink.globals.utilities import ContentAddressableList, AutoNumber, is_component
from psyneulink.globals.keywords \
    import INITIALIZING, EXECUTING, VALIDATE, CONTROL, LEARNING, TRIAL, RUN, COMMAND_LINE, CONTEXT, VALUE, TIME, ALL
from psyneulink.globals.context import ContextState, _get_context


__all__ = [
    'EntriesDict', 'Log', 'LogEntry', 'LogError'
]


LogEntry = namedtuple('LogEntry', 'time, context, value')

TIME_NOT_SPECIFIED = 'Time Not Specified'


class LogTimeScaleIndices(AutoNumber):
    RUN = ()
    TRIAL = ()
    TIME_STEP = ()
NUM_TIME_SCALES = len(LogTimeScaleIndices.__members__)
TIME_SCALE_NAMES = list(LogTimeScaleIndices.__members__)


def _time_string(time):

    # if any(t is not None for t in time ):
    #     run, trial, time_step = time
    #     time_str = "{}:{}:{}".format(run, trial, time_step)
    # else:
    #     time_str = "None"
    # return time_str

    if all(t is not None for t in time ):
        time_str = ":".join([str(i) for i in time])
    else:
        time_str = "None"
    return time_str


#region Custom Entries Dict
# Modified from: http://stackoverflow.com/questions/7760916/correct-useage-of-getter-setter-for-dictionary-values
from collections import MutableMapping
class EntriesDict(MutableMapping,dict):
    """Maintains a Dict of Log entries; assignment of a LogEntry to an entry appends it to the list for that entry.

    The key for each entry is the name of an attribute being logged (usually the `value <Component.value>` of
    the Log's `owner <Log.owner>`.

    The value of each entry is a list, each item of which is a LogEntry.

    When a LogEntry is assigned to an entry:
       - if the entry does not already exist, it is created and assigned a list with the LogEntry as its first item;
       - if it exists, the LogEntry is appended to the list;
       - assigning anything other than a LogEntry raises and LogError exception.

    """
    def __init__(self, owner):

        # Log to which this dict belongs
        self._ownerLog = owner
        # Object to which the log belongs
        self._owner = owner.owner

        # # VERSION THAT USES OWNER'S logPref TO LIST ENTRIES TO BE RECORDED
        # # List of entries (in owner's logPrefs) of entries to record
        # self._recordingList = self._owner.prefs._log_pref.setting

        # # VERSION THAT USES OWNER'S logPref AS RECORDING SWITCH
        # # Recording state (from owner's logPrefs setting)
        # self._recording = self._owner.prefs._log_pref.setting

        super(EntriesDict, self).__init__({})

    def __getitem__(self,key):
        return dict.__getitem__(self,key)

    def __setitem__(self, key, value):

        if not isinstance(value, LogEntry):
            raise LogError("Object other than a {} assigned to Log for {}".format(LogEntry.__name__, self.owner.name))
        try:
        # If the entry already exists, use its value and append current value to it
            self._ownerLog.entries[key].append(value)
            value = self._ownerLog.entries[key]
        except KeyError:
        # Otherwise, initialize list with value as first item
            dict.__setitem__(self,key,[value])
        else:
            dict.__setitem__(self,key,value)

    def __delitem__(self, key):
        dict.__delitem__(self,key)

    def __iter__(self):
        return dict.__iter__(self)

    def __len__(self):
        return dict.__len__(self)

    def __contains__(self, x):
        return dict.__contains__(self,x)
#endregion

#region LogError
class LogError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value

    def __str__(self):
        return repr(self.error_value)
#endregion


class Log:
    """Maintain a Log for an object, which contains a dictionary of logged value(s).

    COMMENT:

    IMPLEMENTATION NOTE: Name of owner Component is aliases to VALUE in loggable_items and logged_items,
    but is the Component's actual name in log_entries

    Description:
        Log maintains a dict (self.entries), with an entry for each attribute of the owner object being logged
        Each entry of self.entries has:
            + a key that is the name of the attribute being logged
            + a value that is a list of sequentially entered LogEntry tuples since recording of the attribute began
            + each tuple has three items:
                - time (CentralClock): when it was recorded in the run
                - context (str): the context in which it was recorded (i.e., where the attribute value was assigned)
                - value (value): the value assigned to the attribute
        An attribute is recorded if:
            - it is one automatically included in logging (see below)
            - it is included in params[LOG_ENTRIES] of the owner object
            - the context of the assignment is above the ContextState specified in the logPref setting of the owner object
        Entry values are added by the setter method for the attribute being logged
        The following entries are automatically included in self.entries for a Mechanism object:
            - the value attribute of every State for which the Mechanism is an owner
            [TBI: - value of every projection that sends to those States]
            - the system variables defined in SystemLogEntries (see declaration above)
            - any variables listed in the params[LOG_ENTRIES] of a Mechanism
        The ContextState class (see declaration above) defines five levels of logging:
            + OFF: No logging for attributes of the owner object
            + VALUE_ASSIGNMENT: Log values only when final value assignment has been during execution
            + EXECUTION: Log values for all assignments during exeuction (e.g., including aggregation of projections)
            + VALIDATION: Log value assignments during validation as well as execution
            + ALL_ASSIGNMENTS:  Log all value assignments (e.g., including initialization)
            Note: ContextState is an IntEnum, and thus its values can be used directly in numerical comparisons

        # Entries can also be added programmtically by:
        #     - including them in the logPref of a PreferenceSet
        #     - using the add_entries() method (see below)
        #     - using the log_entries() method (see below)
        # The owner.prefs.logPref setting contains a list of entries to actively record
        #     - when entries are added to an object's logPref list, the log.add_entries() method is called,
        #         which validates the entries against the object's attributes and SystemLogEntries
        #     - if entries are removed from the object's logPref list, they still remain in the log dict;
        #         they can be deleted from the log dict using the remove_log_entries() method
        #     - data is recorded in an entry using the log_entries() method, which records data to all entries
        #         in the self.owner.prefs.logPrefs list;  this is generally carried out by the update methods
        #         of Category classes in the Function hierarchy (e.g., Process, Mechanism and Projection)
        #         on each cycle of the execution sequence;
        #     - log_entries() adds entries to the self.owner.prefs.logPrefs list,
        #         which will record data for those attributes when logging is active;
        #     - suspend_entries() removes entries from the self.owner.prefs.logPrefs list;
        #         data will not be recorded for those entries when logging is active

        Notes:
        * A list of viable entries should be defined as the classLogEntries class attribute of a Function subclass

    Instantiation:
        A Log object is automatically instantiated for a Function object by Function.__init__(), which assigns to it
            any entries specified in the logPref of the prefs arg used to instantiate the owner object
        Adding an item to self.owner.prefs.logPref will validate and add an entry for that attribute to the log dict

    Initialization arguments:
        - entries (list): list of keypaths for attributes to be logged

    Class Attributes:
        + log (dict)

    Class Methods:
        - add_entries(entries) - add entries to log dict
        - delete_entries(entries, confirm) - delete entries from log dict; confirm=True requires user confirmation
        - reset_entries(entries, confirm) - delete all data from entries but leave them in log dict;
                                                 confirm=True requires user confirmation
        - log_entries(entries) - activate recording of data for entries (adds them to self.owner.prefs.logPref)
        - suspend_entries(entries) - halt recording of data for entries (removes them from self.owner.prefs.logPref)
        - log_entries(entries) - logs the current values of the attributes corresponding to entries
        - print_entries(entries) - prints entry values
        - [TBI: save_log - save log to disk]
    COMMENT

    Attributes
    ----------

    owner : Compoment
        the `Component <Component>` to which the Log belongs (and assigned as its `log <Component.log>` attribute).

    loggable_components : ContentAddressableList
        each item is a Component that is loggable for the Log's `owner <Log.owner>`

    loggable_items : Dict[Component.name: List[LogEntry]]
        identifies Components that can be logged by the owner; the key of each entry is the name of a Component,
        and the value is its currently assigned `ContextState`.

    entries : Dict[Component.name: List[LogEntry]]
        contains the logged information for `loggable_components <Log.loggable_components>`; the key of each entry
        is the name of a Component, and its value is a list of `LogEntry` items for that Component.  Only Components
        for which information has been logged appear in the `entries <Log.entries>` dict.

    logged_items : Dict[Component.name: List[LogEntry]]
        identifies Components that currently have entries in the Log; the key for each entry is the name
        of a Component, and the value is its currently assigned `ContextState`.

    """

    def __init__(self, owner, entries=None):
        """Initialize Log with list of entries

        Each item of the entries list should be a string designating a Component to be logged;
        Initialize self.entries dict, each entry of which has a:
            - key corresponding to a State of the Component to which the Log belongs
            - value that is a list of sequentially logged LogEntry items
        """

        self.owner = owner
        # self.entries = EntriesDict({})
        self.entries = EntriesDict(self)

        if entries is None:
            return

    def set_log_conditions(self, items, log_condition=ContextState.EXECUTION):
        """Specifies items to be logged at the specified `ContextState`\\(s).

        Arguments
        ---------

        items : str, Component, tuple or List of these
            specifies items to be logged;  these must be be `loggable_items <Log.loggable_items>` of the Log.
            Each item must be a:
            * string that is the name of a `loggable_item` <Log.loggable_item>` of the Log's `owner <Log.owner>`;
            * a reference to a Component;
            * tuple, the first item of which is one of the above, and the second a `ContextState` to use for the item.

        log_condition : ContextState : default ContextState.EXECUTION
            specifies `ContextState` to use as the default for items not specified in tuples (see above).
            For convenience, the name of a ContextState can be used in place of its full specification
            (e.g., *EXECUTION* instead of `ContextState.EXECUTION`).

        params_set : list : default None
            list of parameters to include as loggable items;  these must be attributes of the `owner <Log.owner>`
            (for example, Mechanism

        """
        from psyneulink.components.component import Component
        from psyneulink.globals.preferences.preferenceset import PreferenceEntry, PreferenceLevel
        from psyneulink.globals.keywords import ALL

        def assign_log_level(item, level):

            # Handle multiple level assignments (as ContextStates or strings in a list)
            if not isinstance(level, list):
                level = [level]
            levels = ContextState.OFF
            for l in level:
                try:
                    l = ContextState[l.upper()] if isinstance(l, str) else l
                except KeyError:
                    raise LogError("\'{}\' is not a value of {}".
                                   format(l, ContextState.__name__))
                levels |= l
            level = levels

            if not item in self.loggable_items:
                raise LogError("\'{0}\' is not a loggable item for {1} (try using \'{1}.log.add_entries()\')".
                               format(item, self.owner.name))
            try:
                component = next(c for c in self.loggable_components if self._alias_owner_name(c.name) == item)
                component.logPref=PreferenceEntry(level, PreferenceLevel.INSTANCE)
            except AttributeError:
                raise LogError("PROGRAM ERROR: Unable to set ContextState for {} of {}".format(item, self.owner.name))

        if items is ALL:
            for component in self.loggable_components:
                component.logPref = PreferenceEntry(log_condition, PreferenceLevel.INSTANCE)
            # self.logPref = PreferenceEntry(log_condition, PreferenceLevel.INSTANCE)
            return

        if not isinstance(items, list):
            items = [items]

        for item in items:
            if isinstance(item, (str, Component)):
                if isinstance(item, Component):
                    item = item.name
                assign_log_level(item, log_condition)
            else:
                assign_log_level(item[0], item[1])

    def _log_value(self, value, time=None, context=None):
        """Add LogEntry to an entry in the Log

        If **value** is a LogEntry, it is assigned to the entry
        If **context** is a ContextState, it is used to determine whether the entry should be made;
           **time** must be passed;  the name of the ContextState(s) specified are assigned to the context of LogEntry
        Otherwise, uses string (or Component) passed in **context**, or searches stack (see note) to determine the
        context, and uses that to determine the scheduler and, from that, the time;
        If value is None, uses owner's `value <Component.value>` attribute.

        .. note::
            Since _log_value is usually called by the setter for the `value <Component.value>` property of a Component
            (which doesn't/can't receive a context argument), it does not pass a **context** argument to _log_value;
            in that case, _log_value searches the stack for the most recent frame with a context specification, and
            uses that.

        """
        from psyneulink.components.component import Component
        programmatic = False

        if isinstance(value, LogEntry):
            self.entries[self.owner.name] = value

        else:

            if isinstance(context, ContextState):
                context_flags = context
                context = ContextState._get_context_string(context)
                if not time:
                    raise LogError("Use of ContextState ({}) by {} to specify context requires specification of time".
                                   format(context, self.owner.name ))

            # Get context
            else:
                if context is COMMAND_LINE:
                    # If _log_value is being called programmatically,
                    #    flag for later and set context to None to get context from the stack
                    programmatic = True
                    context = None

                # Get context from the stack
                if context is None:
                    curr_frame = inspect.currentframe()
                    prev_frame = inspect.getouterframes(curr_frame, 2)
                    i = 1
                    # Search stack for first frame (most recent call) with a context specification
                    while context is None:
                        try:
                            context = inspect.getargvalues(prev_frame[i][0]).locals['context']
                        except KeyError:
                            # Try earlier frame
                            i += 1
                        except IndexError:
                            # Ran out of frames, so just set context to empty string
                            context = ""
                        else:
                            break

                # If context is a Component object, it must be during its initialization, so assign accordingly:
                if isinstance(context, Component):
                    context = "{} of {}".format(INITIALIZING, context.name)

                # No context was specified in any frame
                if context is None:
                    raise LogError("PROGRAM ERROR: No context specification found in any frame")

                if not isinstance(context, str):
                    raise LogError("PROGRAM ERROR: Unrecognized context specification ({})".format(context))

                # Context is an empty string, but called programmatically
                if not context and programmatic:
                    context = COMMAND_LINE
                    # context = self.owner.prev_context + "FROM " + COMMAND_LINE
                    # context = self.owner.prev_context

                context_flags = _get_context(context)

            log_pref = self.owner.prefs.logPref if self.owner.prefs else None

            # Get time and log value if logging condition is satisfied or called for programmatically
            if (log_pref and log_pref & context_flags) or context_flags & ContextState.COMMAND_LINE:
                time = time or self._get_time(context, context_flags)
                self.entries[self.owner.name] = LogEntry(time, context, value)

        if context is not COMMAND_LINE:
            self.owner.prev_context = context

    def _get_time(self, context, context_flags):
        """Get time from Scheduler of System in which Component is being executed.

        Returns tuple with (run, trial, time_step) if being executed during Processing or Learning
        Otherwise, returns (None, None, None)

        """

        from psyneulink.components.mechanisms.mechanism import Mechanism
        from psyneulink.components.states.state import State
        from psyneulink.components.projections.projection import Projection

        no_time = (None, None, None)

        # Get mechanism to which Component being logged belongs
        if isinstance(self.owner, Mechanism):
            ref_mech = self.owner
        elif isinstance(self.owner, State):
            if isinstance(self.owner.owner, Mechanism):
                ref_mech = self.owner.owner
            elif isinstance(self.owner.owner, Projection):
                ref_mech = self.owner.owner.receiver.owner
            else:
                raise LogError("Logging currently does not support {} (only {}s, {}s, and {}s).".
                               format(self.owner.__class__.__name__,
                                      Mechanism.__name__, State.__name__, Projection.__name__))
        elif isinstance(self.owner, Projection):
            ref_mech = self.owner.receiver.owner
        else:
            raise LogError("Logging currently does not support {} (only {}s, {}s, and {}s).".
                           format(self.owner.__class__.__name__,
                                  Mechanism.__name__, State.__name__, Projection.__name__))

        # MODIFIED 12/11/17 OLD:
        # # Get System in which it is being executed (if any)
        # try:
        #     systems = list(ref_mech.systems.keys())
        #     system = next(s for s in systems if s.name in context)
        # except AttributeError:
        #     # ref_mech has not been assigned to a System
        #     systems = None
        #     system = None
        # except StopIteration:
        #     # ref_mech is assigned to one or more Systems, but not currently being executed within one of them
        #     system = None
        # MODIFIED 12/11/17 NEW:
        # Get System in which it is being (or was last) executed (if any):

        # If called from COMMAND_LINE, get context for last time value was assigned:
        # if context_flags & ContextState.COMMAND_LINE:
        if context_flags & (ContextState.COMMAND_LINE | ContextState.RUN | ContextState.TRIAL):
            execution_context = self.owner.prev_context
            context_flags = _get_context(execution_context)
        else:
            execution_context = context
        try:
            systems = list(ref_mech.systems.keys())
            system = next(s for s in systems if s.name in execution_context)
        except AttributeError:
            # ref_mech has not been assigned to a System
            systems = None
            system = None
        except StopIteration:
            # ref_mech is assigned to one or more Systems, but not currently being executed within one of them
            system = None
        # MODIFIED 12/11/17 END

        if system:
            # FIX: Add VALIDATE?
            if context_flags == ContextState.EXECUTION:
                time = system.scheduler_processing.clock.simple_time
                time = (time.run, time.trial, time.time_step)
            elif context_flags == ContextState.CONTROL:
                time = system.scheduler_processing.clock.simple_time
                time = (time.run, time.trial, time.time_step)
            elif context_flags == ContextState.LEARNING:
                time = system.scheduler_learning.clock.simple_time
                time = (time.run, time.trial, time.time_step)
            else:
                time = None

        # GETS TIME OF LAST RUN OF SYSTEM, BUT NOT NECESSARILY THE COMPONENT (E.G., MECHANISM AND LEARNING)
        # elif systems and (context_flags & ContextState.COMMAND_LINE):
        #     # # Search for the most recently run Scheduler within any of the Systems to which the ref_mech belongs
        #     # # and get its time
        #     # run_times = []
        #     # for s in systems:
        #     #     run_times.append((s.scheduler_processing.date_last_run_end, s.scheduler_processing.clock.simple_time))
        #     #     run_times.append((s.scheduler_learning.date_last_run_end, s.scheduler_learning.clock.simple_time))
        #     # gmt, time = max(run_times, key=lambda x : x[0])
        #     # time = (time.run, time.trial, time.time_step)

        else:
            if self.owner.verbosePref:
                offender = "\'{}\'".format(self.owner.name)
                if ref_mech is not self.owner:
                    offender += " [{} of {}]".format(self.owner.__class__.__name__, ref_mech.name)
                warnings.warn("Attempt to log {} which is not in a System (logging is currently supported only "
                              "when running Components within a System".format(offender))
            time = None

        return time or no_time

    @tc.typecheck
    def log_values(self, entries):
        """Log the value of one or more Components programmatically.

        This can be used to "manually" enter the `value <Component.value>` of any of a Component's `loggable_items
        <Component.loggable_items>` (including its own `value <Component.value>`) in its `log <Component.log>`.
        The context item of its `LogEntry` is assigned *COMMAND_LINE*.  If the call to log_values is made while a
        System to which the Component belongs is being run (e.g., in a **call_before..** or **call_after...** argument
        of its `run <System_Base.run>` method), then the time of the LogEntry is assigned the value of the `Clock` of
        the System's `scheduler_processing` or `scheduler_learning`, whichever is currently executing
        (see `System_Scheduler`).

        Arguments
        ---------

        entries : string, Component or list containing either : default ALL
            specifies the Components, the current `value <Component.value>`\\s of which should be added to the Log.
            they must be `loggable_items <Log.loggable_items>` of the owner's Log. If **entries** is *ALL* or is not
            specified, then the `value <Component.value>`\\s of all `loggable_items <Log.loggable_items>` are logged.
        """
        entries = self._validate_entries_arg(entries)

        # Validate the Component field of each LogEntry
        for entry in entries:
            self._log_value(self.loggable_components[self._dealias_owner_name(entry)].value, context=COMMAND_LINE)

    def clear_entries(self, entries=ALL, delete_entry=True, confirm=False):
        """Clear one or more entries either by deleting the entry or just removing its data.

        Arguments
        ---------

        entries : string, Component or list containing either : default ALL
            specifies the entries of the Log to be cleared;  they must be `loggable_items
            <Log.loggable_items>` of the Log that have been logged (i.e., are also `logged_items <Log.logged_items>`).
            If **entries** is *ALL* or is not specified, then all `logged_items <Log.logged_items>` are cleared.

        delete_entry : bool : default True
            specifies whether to delete the entry (if `True`) from the log to which it belongs, or just
            delete the data, but leave the entry itself (if `False`).

            .. note::
                This option is included for generality and potential future features, but is not advised;
                the Log interface (e.g., the `logged_items <Log.logged_items>` interface generally assumes that
                the only `entries <Log.entries>` in a log are ones with data.

        confirm : bool : default False
            specifies whether user confirmation is required before clearing the entries.

            .. note::
                If **confirm** is `True`, only a single confirmation will occur for a list or *ALL*

        """

        entries = self._validate_entries_arg(entries)

        # If any entries remain
        if entries:
            if confirm:
                delete = input("\nAll data will be deleted from {0} in the Log for {1}.  Proceed? (y/n)".
                               format(entries,self.owner.name))
                while delete != 'y' and delete != 'y':
                    input("\nDelete all data from entries? (y/n)")
                if delete == 'n':
                    return

            # Clear entries
            for entry in entries:
                self.logged_entries[entry]=[]
                if delete_entry:
                # Delete the entire entry from the log to which it belongs
                    del self.loggable_components[entry].log.entries[entry]
                else:
                    # Delete the data for the entry but leave the entry itself in the log to which it belongs
                    del self.logged_entries[entry][0:]
                assert True

    @tc.typecheck
    def print_entries(self,
                      entries:tc.optional(tc.any(str, list, is_component))=ALL,
                      width:int=120,
                      display:tc.any(tc.enum(TIME, CONTEXT, VALUE, ALL), list)=ALL,
                      long_context=False
                      ):
        """
        print_entries(          \
              entries=ALL,      \
              width=120,        \
              display=None      \
              long_context=Full \
            )

        Print summary of the Log's entries in a (human-readable) table format.

        Arguments
        ---------

        entries : string, Component or list containing either : default ALL
            specifies the entries of the Log to printed;  they must be `loggable_items <Log.loggable_items>` of the
            Log that have been logged (i.e., are also `logged_items <Log.logged_items>`).
            If **entries** is *ALL* or is not specified, then all `logged_items <Log.logged_items>` are printed.

        width : int : default 120
            specifies the width of the display. The widths of each column are adjusted accordingly, and based
            on which items are displayed (see **display** below);  information that does not fit within its column's
            width is truncated and suffixes with an ellipsis.

        display : TIME, CONTEXT, VALUE, a list containing any of these, or ALL : default ALL
            specifies the information items to display.  The name of the entry is always displayed, followed by the 
            specified items;  the widths of the columns for the items is dynamically adjusted, based on how many
            are specified, allowing more information about one to be shown by omitting others (this is useful 
            if the context strings are long and/or the values are arrays).

        long_context : bool : default False
            specifies the use of the full context string in the display;  this can be informative, but can also take up
            more space in each line of the display.
            
        """

        entries = self._validate_entries_arg(entries, logged=True)

        if not entries:
            return None

        class options(IntEnum):
            NONE = 0
            TIME = 2
            CONTEXT = 4
            VALUE = 8
            ALL = TIME + CONTEXT + VALUE

        display = display or ALL
        if not isinstance(display, list):
            display = [display]

        # Set option_flags for specified options
        option_flags = options.NONE
        if TIME in display:
            option_flags |= options.TIME
        if CONTEXT in display:
            option_flags |= options.CONTEXT
        if VALUE in display:
            option_flags |= options.VALUE
        if ALL in display:
            option_flags = options.ALL

        # Default widths
        full_width = width
        item_name_width = 15
        time_width = 10
        context_width = 70
        value_width = 30
        spacer = ' '
        value_spacer_width = 3
        value_spacer = " ".ljust(value_spacer_width)
        base_width = item_name_width

        # Set context_width based on long_context option (length of context string) or context flags
        if option_flags & options.CONTEXT:
            c_width = 0
            for entry in entries:
                for datum in self.logged_entries[entry]:
                    if long_context:
                        context = datum.context
                    else:
                        context = ContextState._get_context_string(_get_context(datum.context))
                    c_width = max(c_width, len(context))
            context_width = min(context_width, c_width)

        # Set other widths based on options:
        # FIX: "ALGORITHMIZE" THIS:
        if option_flags == options.TIME:
            pass
        elif option_flags == options.CONTEXT:
            context_width = full_width - base_width
        elif option_flags == options.VALUE:
            value_width = full_width - base_width
        elif option_flags == options.TIME + options.CONTEXT:
            context_width = full_width - time_width - base_width
        elif option_flags == options.TIME + options.VALUE:
            value_width = full_width - time_width - base_width
        elif option_flags == options.CONTEXT + options.VALUE:
            context_width = full_width - value_width
            value_width = full_width - context_width
        elif option_flags == options.ALL:
            value_width = full_width - context_width
        else:
            raise LogError("PROGRAM ERROR:  unrecognized state of option_flags: {}".format(option_flags))

        header = "Logged Item:".ljust(item_name_width, spacer)
        if options.TIME & option_flags:
            header = header + TIME.capitalize().ljust(time_width, spacer)
        if options.CONTEXT & option_flags:
            header = header + " " + CONTEXT.capitalize().ljust(context_width, spacer)
        if options.VALUE & option_flags:
            header = header + value_spacer + " " + VALUE.capitalize()
            # header = header + value_spacer + VALUE.capitalize()

        print("\nLog for {0}:".format(self.owner.name))
        print('\n'+header+'\n')

        # Sort for consistency of reporting
        # entry_names_sorted = sorted(self.logged_entries.keys())
        entry_names_sorted = sorted(entries)
        # spacer = '_'
        # for entry_name in self.logged_entries:
        for entry_name in entry_names_sorted:
            try:
                datum = self.logged_entries[entry_name]
            except KeyError:
                warnings.warn("{0} is not an entry in the Log for {1}".
                      format(entry_name, self.owner.name))
            else:
                import numpy as np
                for i, item in enumerate(datum):

                    time, context, value = item

                    entry_name = self._alias_owner_name(entry_name)
                    data_str = repr(entry_name).ljust(item_name_width, spacer)

                    if options.TIME & option_flags:
                        time_str = _time_string(time)
                        data_str = data_str + time_str.ljust(time_width)

                    if options.CONTEXT & option_flags:
                        if long_context:
                            # Use context from LogEntry
                            context = repr(context)
                        else:
                            # Get names of ContextState flag(s) from parse of context string
                            context = ContextState._get_context_string(_get_context(context))
                        if len(context) > context_width:
                            context = context[:context_width-3] + "..."
                        data_str = data_str + context.ljust(context_width, spacer)

                    if options.VALUE & option_flags:
                        value = str(value).replace('\n',',')
                        if len(value) > value_width:
                            value = value[:value_width-3].rstrip() + "..."
                        format_str = "{{:2.{0}}}".format(value_width)
                        data_str = data_str + value_spacer + format_str.format(value).ljust(value_width)

                    print(data_str)

                if len(datum) > 1:
                    print("\n")

    @tc.typecheck
    def nparray(self,
                entries=None,
                header:bool=True,
                owner_name:bool=False
                ):
        """
        nparray(                 \
            entries=None,        \
            header:bool=True,    \
            owner_name=False):   \
            )

        Return a 2d numpy array with headers (optional) and values for the specified entries.

        Each row (axis 0) is a time series, with each item in each row the data for the corresponding time point.
        Rows are ordered in the same order as Components are specified in the **entries** argument.

        If all of the data for every entry has a time value (i.e., the time field of its LogEntry is not `None`),
        then the first three rows are time indices for the run, trial and time_step of each data item, respectively.
        Each subsequent row is the times series of data for a given entry.  If there is no data for a given entry
        at a given time point, it is entered as `None`.

        If any of the data for any entry does not have a time value (e.g., if that Component was not run within a
        System), then all of the entries must have the same number of data (LogEntry) items, and the first row is a
        sequential index (starting with 0) that simply designates the data item number.

        .. note::
           For data without time stamps, the nth items in each entry correspond (i.e., ones in the same column)
           are not guaranteed to have been logged at the same time point.

        If header is `True`, the first item of each row is a header field: for time indices it is either "Run",
        "Trial", and "Time_step", or "Index" if any data are missing time stamps.  For subsequent rows it is the name
        of the Component logged in that entry (see **owner_name** argument below for formatting).


        Arguments
        ---------

        entries : string, Component or list containing either : default ALL
            specifies the entries of the Log to be included in the output;  they must be `loggable_items
            <Log.loggable_items>` of the Log that have been logged (i.e., are also `logged_items <Log.logged_items>`).
            If **entries** is *ALL* or is not specified, then all `logged_items <Log.logged_items>` are included.

        COMMENT:
        time : TimeScale or ALL : default ALL
            specifies the "granularity" of how the time of an entry is reported.  *ALL* (same as `TIME_STEP
            <TimeScale.TIME_STEP>) reports every entry in the Log in a separate column (axis 1) of the np.array
            returned.
        COMMENT

        header : bool : default True
            specifies whether or not to include a header in each row with the name of the Component for that entry.

        owner_name : bool : default False
            specifies whether or not to include the Log's `owner <Log.owner>` in the header of each field;
            if it is True, the format of the header for each field is "<Owner name>[<entry name>]";
            otherwise, it is "<entry name>".

        Returns:
            2d np.array
        """

        entries = self._validate_entries_arg(entries, logged=True)

        if not entries:
            return None

        if owner_name is True:
            owner_name_str = self.owner.name
            lb = "["
            rb = "]"
        else:
            owner_name_str = lb = rb = ""

        header = 1 if header is True else 0

        # Get time values for all entries and sort them
        time_values = []
        for entry in entries:
            time_values.extend([item.time
                                for item in self.logged_entries[entry]
                                if all(i is not None for i in item.time)])
        # Insure that all time values are assigned, get rid of duplicates, and sort
        if all(all(i is not None for i in t) for t in time_values):
            time_values = sorted(list(set(time_values)))
        npa = []

        # Create time rows (one for each time scale)
        if time_values:
            for i in range(NUM_TIME_SCALES):
                row = [[t[i]] for t in time_values]
                if header:
                    time_header = [TIME_SCALE_NAMES[i].capitalize()]
                    row = [time_header] + row
                npa.append(row)
        # If any time values are empty, revert to indexing the entries;
        #    this requires that all entries have the same length
        else:
            max_len = max([len(self.logged_entries[e]) for e in entries])

            # If there are no time values, only support entries of the same length
            if not all(len(self.logged_entries[e])==len(self.logged_entries[entries[0]])for e in entries):
                raise LogError("nparray output requires that all entries have time values or are of equal length")

            npa = np.arange(max_len).reshape(max_len,1).tolist()
            if header:
                npa = [["Index"] + npa]
            else:
                npa = [npa]

        # For each entry, iterate through its LogEntry tuples:
        #    for each LogEntry tuple, check whether its time matches that of the next column:
        #        if so, enter it in the entry's list
        #        if not, enter `None` and check for a match in the next time column
        for entry in entries:
            row = []
            time_col = iter(time_values)
            for datum in self.logged_entries[entry]:
                if time_values:
                    # time_col = iter(time_values)
                # # MODIFIED 12/14/17 OLD:
                #     while datum.time != next(time_col,None):
                #         row.append(None)
                # value = None if datum.value is None else np.array(datum.value).tolist()
                # row.append(value)
                # MODIFIED 12/14/17 NEW:
                    for i in range(len(time_values)):
                        time = next(time_col,None)
                        if time is None:
                            break
                        if datum.time != time:
                            row.append(None)
                            continue
                        value = None if datum.value is None else datum.value.tolist()
                        row.append(value)
                        break
                else:
                    value = None if datum.value is None else datum.value.tolist()
                    row.append(value)
                # MODIFIED 12/14/17 END

            if header:
                entry_header = "{}{}{}{}".format(owner_name_str, lb, self._alias_owner_name(entry), rb)
                row = [entry_header] + row
            npa.append(row)

        npa = np.array(npa, dtype=object)
        return(npa)

    @tc.typecheck
    def csv(self, entries=None, owner_name:bool=False, quotes:tc.optional(tc.any(bool, str))="\'"):
        """
        csv(                           \
            entries=None,              \
            owner_name=False,          \
            quotes=\"\'\"              \
            )

        Returns a CSV-formatted string with headers and values for the specified entries.

        Each row (axis 0) is a time point, beginning with the time stamp and followed by the data for each
        Component at that time point, in the order they are specified in the **entries** argument. If all of the data
        for every Component have time values, then the first three items of each row are the time indices for the run,
        trial and time_step of that time point, respectively, followed by the data for each Component at that time
        point;  if a Component has no data for a time point, `None` is entered.

        If any of the data for any Component does not have a time value (i.e., it has `None` in the time field of
        its `LogEntry`) then all of the entries must have the same number of data (LogEntry) items, and the first item
        of each row is a sequential index (starting with 0) that designates the data item number.

        .. note::
           For data without time stamps, items in the same row are not guaranteed to refer to the same time point.

        The **owner_name** argument can be used to prepend the header for each Component with its owner.
        The **quotes** argument can be used to suppress or specifiy quotes to use around numeric values.


        Arguments
        ---------

        entries : string, Component or list containing either : default ALL
            specifies the entries of the Log to be included in the output;  they must be `loggable_items
            <Log.loggable_items>` of the Log that have been logged (i.e., are also `logged_items <Log.logged_items>`).
            If **entries** is *ALL* or is not specified, then all `logged_items <Log.logged_items>` are included.

        owner_name : bool : default False
            specifies whether or not to include the Component's `owner <Log.owner>` in the header of each field;
            if it is True, the format of the header for each field is "<Owner name>[<entry name>]"; otherwise,
            it is "<entry name>".

        quotes : bool, str : default '
            specifies whether or not to enclose numeric values in quotes (may be useful for arrays);
            if not specified or `True`, single quotes are used for *all* items;
            if specified with a string, that is used in place of single quotes to enclose *all* items;
            if `False` or `None`, single quotes are used for headers (the items in the first row), but no others.

        Returns:
            CSV-formatted string
        """

        # Get and transpose nparray of entries
        try:
            npa = self.nparray(entries=entries, header=True, owner_name=owner_name)
        except LogError as e:
            raise LogError(e.args[0].replace('nparray', 'csv'))
        npaT = npa.T

        if not quotes:
            quotes = ''
        elif quotes is True:
            quotes = '\''

        # Headers
        csv = "\'" + "\', \'".join(i[0] if isinstance(i, list) else i for i in npaT[0]) + "\'"
        # csv = "\'" + "\', \'".join(npaT[0]) + "\'"
        # Data
        for i in range(1, len(npaT)):
            csv += '\n' + ', '.join([str(j) for j in [str(k).replace(',','') for k in npaT[i]]]).\
                replace('[[',quotes).replace(']]',quotes).replace('[',quotes).replace(']',quotes)
        csv += '\n'

        return(csv)

    def _validate_entries_arg(self, entries, loggable=True, logged=False):
        from psyneulink.components.component import Component

        # If ALL, set entries to all entries in self.logged_entries
        if entries is ALL or entries is None:
            entries = self.logged_entries.keys()

        # If entries is a single entry, put in list for processing below
        if isinstance(entries, (str, Component)):
            entries = [entries]

        # Make sure all entries are the names of Components
        entries = [entry.name if isinstance(entry, Component) else entry for entry in entries ]

        # Validate entries
        for entry in entries:
            if loggable:
                if self._alias_owner_name(entry) not in self.loggable_items:
                    raise LogError("{0} is not a loggable attribute of {1}".format(repr(entry), self.owner.name))
            if logged:
                if entry not in self.logged_entries:
                    # raise LogError("{} is not currently being logged by {} (try using set_log_conditions)".
                    #                format(repr(entry), self.owner.name))
                    print("\n{} is not currently being logged by {} or has not data (try using set_log_conditions)".
                          format(repr(entry), self.owner.name))
        return entries

    def _alias_owner_name(self, name):
        """Alias name of owner Component to VALUE in loggable_items and logged_items
        Component's actual name is preserved and used in log_entries (i.e., as entered by _log_value)
        """
        return VALUE if name is self.owner.name else name


    def _dealias_owner_name(self, name):
        """De-alias VALUE to name of owner
        """
        return self.owner.name if name is VALUE else name

    @property
    def loggable_items(self):
        """Return dict of loggable items.

        Keys are names of the Components, values their ContextStates
        """
        # FIX: The following crashes during init as prefs have not all been assigned
        # return {key: value for (key, value) in [(c.name, c.logPref.name) for c in self.loggable_components]}

        loggable_items = {}
        for c in self.loggable_components:
            name = self._alias_owner_name(c.name)
            try:
                # log_pref_names = c.logPref.name
                log_pref_names = ContextState._get_context_string(c.logPref)
            except:
                log_pref_names = None
                # log_pref_names = ContextState._get_condition_string(c.logPref)
            loggable_items[name] = log_pref_names
        return loggable_items

    @property
    def loggable_components(self):
        """Return a list of owner's Components that are loggable

        The loggable items of a Component are the Components (typically States) specified in the _logagble_items
        property of its class, and its own `value <Component.value>` attribute.
        """
        from psyneulink.components.component import Component

        try:
            loggable_items = ContentAddressableList(component_type=Component, list=self.owner._loggable_items)
            loggable_items[self.owner.name] = self.owner
        except AttributeError:
            return []
        return loggable_items

    @property
    def logged_items(self):
        """Dict of items that have logged `entries <Log.entries>`, indicating their specified `ContextState`.
        """
        log_condition = 'ContextState.'
        # Return ContextState for items in log.entries

        logged_items = {key: value for (key, value) in
                        # [(l, self.loggable_components[l].logPref.name)
                        [(self._alias_owner_name(l), self.loggable_items[self._alias_owner_name(l)])
                         for l in self.logged_entries.keys()]}

        return logged_items

    @property
    def logged_entries(self):
        entries = {}
        for e in self.loggable_components:
            entries.update(e.log.entries)
        return entries

    # def save_log(self):
    #     print("Saved")

def _log_trials_and_runs(composition, curr_condition:tc.enum(ContextState.TRIAL, ContextState.RUN), context):
    # FIX: ALSO CHECK TIME FOR scheduler_learning, AND CHECK DATE FOR BOTH, AND USE WHICHEVER IS LATEST
    # FIX:  BUT WHAT IF THIS PARTICULAR COMPONENT WAS RUN IN THE LAST TIME_STEP??
    for mech in composition.mechanisms:
        for component in mech.log.loggable_components:
            if component.logPref & curr_condition:
                # value = LogEntry((composition.scheduler_processing.clock.simple_time.run,
                #                   composition.scheduler_processing.clock.simple_time.trial,
                #                   composition.scheduler_processing.clock.simple_time.time_step),
                #                  # context,
                #                  curr_condition,
                #                  component.value)
                # component.log._log_value(value=value, context=context)
                component.log._log_value(value=component.value, context=curr_condition.name)

        for proj in mech.afferents:
            for component in proj.log.loggable_components:
                if component.logPref & curr_condition:
                    # value = LogEntry((composition.scheduler_processing.clock.simple_time.run,
                    #                   composition.scheduler_processing.clock.simple_time.trial,
                    #                   composition.scheduler_processing.clock.simple_time.time_step),
                    #                  context,
                    #                  component.value)
                    # component.log._log_value(value, context)
                    component.log._log_value(value=component.value, context=curr_condition.name)


    # FIX: IMPLEMENT ONCE projections IS ADDED AS ATTRIBUTE OF Composition
    # for proj in composition.projections:
    #     for component in proj.log.loggable_components:
    #         if component.logPref & curr_condition:
    #             value = LogEntry((composition.scheduler_processing.clock.simple_time.run,
    #                               composition.scheduler_processing.clock.simple_time.trial,
    #                               composition.scheduler_processing.clock.simple_time.time_step),
    #                              context,
    #                              component.value)
    #             component.log._log_value(value, context)
