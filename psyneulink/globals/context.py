# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
#
# ********************************************  System Defaults ********************************************************

from enum import IntEnum

from psyneulink.globals.keywords import INITIALIZING, VALIDATE, EXECUTING, CONTROL, LEARNING


class Context():
    composition = None
    string = ""


# FIX: REPLACE WITH Flags and auto IF/WHEN MOVE TO Python 3.6
class LogCondition(IntEnum):
    """Specifies levels of logging, as descrdibed below."""
    OFF = 0
    """No recording."""
    INITIALIZATION =     1<<1       # 2
    """Record value during initial assignment."""
    VALIDATION =         1<<2       # 4
    """Record value during validation."""
    EXECUTION =          1<<3       # 8
    """Record all value assignments during any execution of the Component."""
    PROCESSING =         1<<4       # 16
    """Record all value assignments during processing phase of Composition execution."""
    LEARNING =           1<<5       # 32
    """Record all value assignments during learning phase of Composition execution."""
    CONTROL =            1<<6       # 64
    """Record all value assignments during control phase of Composition execution."""
    # FIX: TRIAL, RUN, VALUE_ASSIGNMENT & FINAL NOT YET IMPLEMENTED:
    TRIAL =              1<<7       # 128
    """Record value at the end of a TRIAL."""
    RUN =                1<<8       # 256
    """Record value at the end of a RUN."""
    VALUE_ASSIGNMENT =   1<<9       # 512
    # """Record final value assignments during Composition execution."""
    FINAL =             1<<10       # 1024
    # """Synonym of VALUE_ASSIGNMENT."""
    COMMAND_LINE =      1<<11       # 2048
    ALL_ASSIGNMENTS = \
        INITIALIZATION | VALIDATION | EXECUTION | PROCESSING | LEARNING | CONTROL | VALUE_ASSIGNMENT | FINAL
    """Record all value assignments."""

    # @classmethod
    # def _log_level_max(cls):
    #     return max([cls[i].value for i in list(cls.__members__) if cls[i] is not LogCondition.ALL_ASSIGNMENTS])

    @classmethod
    def _get_condition_string(cls, condition, string=None):
        """Return string with the names of all flags that are set in **condition**, prepended by **string**"""
        if string:
            string += ": "
        else:
            string = ""
        flagged_items = []
        # If OFF or ALL_ASSIGNMENTS, just return that
        if condition in (LogCondition.ALL_ASSIGNMENTS, LogCondition.OFF):
            return condition.name
        # Otherwise, append each flag's name to the string
        for c in list(cls.__members__):
            # Skip ALL_ASSIGNMENTS (handled above)
            if c is LogCondition.ALL_ASSIGNMENTS.name:
                continue
            if LogCondition[c] & condition:
               flagged_items.append(c)
        string += ", ".join(flagged_items)
        return string


def _get_log_context(context):

    if isinstance(context, LogCondition):
        return context
    context_flag = LogCondition.OFF
    if INITIALIZING in context:
        context_flag |= LogCondition.INITIALIZATION
    if VALIDATE in context:
        context_flag |= LogCondition.VALIDATION
    if EXECUTING in context:
        context_flag |= LogCondition.EXECUTION
    if CONTROL in context:
        context_flag |= LogCondition.CONTROL
    if LEARNING in context:
        context_flag |= LogCondition.LEARNING
    if context == LogCondition.TRIAL.name:
        context_flag |= LogCondition.TRIAL
    if context == LogCondition.RUN.name:
        context_flag |= LogCondition.RUN
    if context == LogCondition.COMMAND_LINE.name:
        context_flag |= LogCondition.COMMAND_LINE
    return context_flag
