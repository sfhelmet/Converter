state(idle).
state(active).
state(error).
state(final).
initial(idle).
final(final).

entry_pseudostate(active_skip_config_entry, reading).	% active superstate is implied
exit_pseudostate(active_exit, active).			    % the out transition may be guarded

transition(idle, active, event(call, activate), nil, nil).
transition(idle, active_skip_config_entry, event(call, 'skip configuring'), nil, nil).
transition(error, active, event(call, reset), nil, nil).
transition(active, idle, event(call, deactivate), nil, nil).
transition(idle, final, event(call, shutoff), nil, nil).
transition(active_exit, error, nil, nil, nil).	% see exit_pseudostate

superstate(active, reading).