import time

CALLBACK_EXPIRED_EVENT = 'Listener Expired'
CALLBACK_REGISTERED_EVENT = 'New Listener Registered'
ALL_EVENTS = '*'

GLOBAL_EVENTS = [
    ALL_EVENTS,
    CALLBACK_EXPIRED_EVENT,
    CALLBACK_REGISTERED_EVENT,
]

__callbacks = {}

def emit(event: str, *args, **kwargs) -> None:
    '''
    Fires off the string event and notifies all registered (non expired) callables of the event. Note, if the callable returns True on its call, we will consider the event consumed and will not continue notifying other registered listeners

    :param event (string):
        This is the event string that is fired
    :param args (iterable, Optional):
        Any additional args to pass to the callable on the event fire
    :param kwargs (dict, Optional):
        Any additional kwargs to pass.
        Note: kwargs['event'] will be the string event that was fired, and this will override any item associated with kwargs['event']. Consider 'event' a reserved keyword

    :return None:
    '''
    for callback in _get_callbacks(event):
        kwargs['event'] = event
        consumed = callback(*args, **kwargs)
        if consumed is True:
            break

def register(event: str, callback: callable, ttl: float=float('inf')) -> None:
    '''
    Registers a callback for when the listed event is fired

    :param event (string):
        The string event to listen for. There are some global events that can be found at event_manager.GLOBAL_EVENTS. Alternatively, provide a string to listen for. Note, event can be '*', to which every event that is fired, this callback will be called
    :param callback (callable):
        The callable to call when a matching event is fired.
        Note: You can optional return a True from your callable to indicate that the fired event was consumed.
        @see event_manager.emit
    :param ttl (float, Optional):
        The time to live for the callback. If not provided, defaults to infinity

    :return None:
    '''
    if event not in __callbacks.keys():
        __callbacks[event] = {}
    __callbacks[event][callback] = ttl if ttl == float('inf') else time.time() + ttl
    emit(CALLBACK_REGISTERED_EVENT, callback, ttl)

def unregister(event: str, callback: callable) -> None:
    '''
    Removes the listed callback as a callback for the provided event

    :param event (string):
        The string event to unregister from
    :param callback (callable):
        The callback to unregister

    :return None:
    '''
    del __callbacks[event][callback]

def _get_callbacks(event: str) -> list:
    '''
    Gets a list of all non-expired callbacks for the provided event. 
    Note, auto expires any callbacks that have met/passed their ttl

    :param event (string):
        The string event to get callbacks for

    :return list:
    '''
    callbacks = []
    for _event in [event, '*']:
        for callback, ttl in __callbacks.get(_event, dict()).items():
            if time.time() >= ttl:
                unregister(_event, callback)
                emit(CALLBACK_EXPIRED_EVENT, callback)
                continue
            callbacks.append(callback)
    return callbacks
