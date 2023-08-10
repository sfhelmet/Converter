state(idle).        state(error).       state(final).
state(pre_idle).    state(configuring). state(reading).
state(active_exit). state(activated).   state(efinal).
state(s11).         state(s12).         state(s21).
state(s22).         state(s31).         state(s41).
state(s71).         state(s91).         state(s92).
initial(pre_idle).  final(final).
alias(final, "").   alias(efinal, "").
transition(activated, s11, event(call, reset), nil, action(log, "ABORT 'Make Siren Sound'")).
transition(s11, s12, nil, nil, action(exec, "echo('Exit Emergency');")).
transition(s12, reading, nil, nil, action(log, "START 'Slow blinking red LED'")).
transition(activated, s21, event(call, deactivate), nil, action(log, "ABORT 'Make Siren Sound'")).
transition(s21, s22, nil, nil, action(exec, "echo('Exit Emergency');")).
transition(configuring, s31, event(timeout, "2:00"), nil, 
    action(exec, "echo('Exit configuring mode');")).
transition(s31, active_exit, nil, nil, action(exec, "beep();")).
transition(configuring, s41, event(call, cancel), nil, 
    action(exec, "echo('Exit configuring mode');")).
transition(reading, s71, event(call, set), nil, action(log, "ABORT 'Slow blinking red LED'")).
transition(s71, configuring, nil, nil, action(exec, "echo('Configuring mode');")).
transition(reading, s91, event(when, "tCurrent >= tThreshold"), nil, 
    action(log, "ABORT 'Slow blinking red LED'")).
transition(s91, s92, nil, nil, action(exec, "sendNotification();")).
transition(s92, activated, nil, nil, action(log, "START 'Make Siren Sound'")).
transition(idle, final, event(call, shutoff), nil, action(log, "System Shutdown")).
transition(activated, efinal, event(after, "2:00"), nil, nil).
transition(pre_idle, idle, nil, nil, action(log, "System Startup")).
transition(active_exit, error, nil, nil, action(log, "Green LED OFF")).
transition(configuring, configuring, event(set, tThreshold), nil, action(exec, "doubleBeep();")).
transition(configuring, configuring, event(call, done), 
    "tThreshold <= tCurrent", action(exec, "generateError();")).
transition(s41, s12, nil, nil, action(exec, "longBeep();")).
transition(configuring, s12, event(call, done), 
    "tThreshold > tCurrent", action(exec, "echo('Exit configuring mode');")).
transition(idle, s12, event(call, "skip configuring"), nil, action(log, "Green LED ON")).
transition(idle, s71, event(call, activate), nil, action(log, "Green LED ON")).
transition(error, s71, event(call, reset), nil, action(log, "Green LED ON")).
transition(s22, pre_idle, nil, nil, action(log, "Green LED OFF")).
transition(activated, s11, event(completed, emergency), nil, 
    action(log, "STOP 'Make Siren Sound'")).
transition(efinal, s11, nil, nil, action(log, "STOP 'Make Siren Sound'")).
transition(configuring, s22, event(call, deactivate), nil, 
    action(exec, "echo('Exit configuring mode');")).
transition(reading, s22, event(call, deactivate), nil, 
    action(log, "ABORT 'Slow blinking red LED'")).
