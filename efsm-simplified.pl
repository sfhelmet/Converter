% state names are globally unique, use alias/2 if not
%----------------------------------------------------------------

% page 1
%----------------------------------------------------------------

state(idle).
state(active).
state(error).
state(final).
initial(idle).
final(final).

alias(final, '').

entry_pseudostate(active_skip_config_entry, reading).	% active superstate is implied
exit_pseudostate(active_exit, active).			    % the out transition may be guarded

transition(idle, active, event(call, activate), nil, nil).
transition(idle, active_skip_config_entry, event(call, 'skip configuring'), nil, nil).
trasition(error, active, event(call, reset), nil, nil).
transition(active, idle, event(call, deactivate), nil, nil).
transition(idle, final, event(call, shutoff), nil, nil).
transition(active_exit, error, nil, nil, nil).	% see exit_pseudostate

% page 2
%----------------------------------------------------------------

superstate(active, configuring).
superstate(active, reading).
superstate(active, emergency).
initial(configuring).						% configuring is a level 2 state: i.o.w. superstate(_, configuring) is true.


onentry_action(active, action(log, "Green LED ON")).
onexit_action(active, action(log, "Green LED OFF")).
onentry_action(configuring, action(exec, "echo('Configuring mode');")).
onexit_action(configuring, action(exec, "echo('Exit configuring mode');")).

% do_action/2 receives a process
% do_action/5 alternatively receives, process, onstart, onstop, and onabort js codes. (TBD)
do_action(reading, proc('Slow blinking red LED')).

transition(configuring, reading, event(call, cancel), nil, action(exec, "longBeep();")).
transition(configuring, active_exit, event(timeout, "2:00"), nil, action(exec, "beep();")).	% perhaps we can rename inactivity to timeout
transition(reading, emergency, event(when, "tCurrent >= tThreshold"), nil, action(exec, "sendNotification();")).
transition(reading, configuring, event(call, set), nil, nil).
transition(emergency, reading, event(call, reset), nil, nil).
transition(emergency, reading, nil, nil, nil).	% completed emergency
transition(configuring, reading, event(call, done), "tThreshold > tCurrent", nil, nil).

internal_transition(configuring, event(set, tThreshold), nil, action(exec, "doubleBeep();")).
internal_transition(configuring, event(call, done), "tThreshold <= tCurrent", action(exec, "generateError();")).

% page 3
%----------------------------------------------------------------

do_action(emergency, proc('Make Siren Sound')).
onexit_action(emergency, action(exec,"echo('Exit Emergency');")).

superstate(emergency, activated).
superstate(emergency, efinal).
initial(activated).
final(efinal).
alias(efinal, '').

transition(activated, efinal, event(after, "2:00"), nil, nil, nil).