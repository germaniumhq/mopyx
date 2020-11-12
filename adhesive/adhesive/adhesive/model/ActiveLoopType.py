from enum import Enum


class ActiveLoopType(Enum):
    """
    Describes if this event is part of a loop. If it is, this impacts the
    routing of the element, since loops need to potentially create multiple
    execution tokens, as well as execute the task multiple times, or not at
    all.
    """
    # an initial loop is an unknown type of loop. There is a loop condition,
    # but we haven't yet executed the task, nor we know what is the condition
    # returning. If the loop condition evaluates to falsy the task will not be
    # executed, and the token will be routed further.
    INITIAL = 'INITIAL'

    # If the initial event doesn't evaluate to anything it's marked as
    # INITIAL_EMPTY so the routing can continue. If it's still in INITIAL, the
    # event is discarded, since we have the other executions happening as
    # either CONDITIONs or COLLECTIONs
    INITIAL_EMPTY = 'INITIAL_EMPTY'

    # If the condition returned something that's not a collection, this becomes
    # a condition loop. This means the execution is now serial (regardless of
    # the parallel flag), and it will continue executing as long as the
    # condition still returns true.
    CONDITION = 'CONDITION'

    # If the condition returned a collection, the tokens for the loop are
    # already created and will only execute once.
    COLLECTION = 'COLLECTION'

    # If the collection is bound to a serial loop, the tokens are returned one
    # by one, and the remaining items are WAITING until the previous ones
    # execute.
    COLLECTION_SERIAL = 'COLLECTION_SERIAL'
