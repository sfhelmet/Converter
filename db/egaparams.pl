transition(activated, s11, event(call, reset), nil, action(log, "ABORT 'Make Siren Sound'")).
transition(s11, s12, nil, nil, action(exec, "echo('Exit Emergency');")).
transition(activated, s21, event(call, deactivate), nil, action(log, "ABORT 'Make Siren Sound'")).
transition(configuring, s31, event(timeout, "2:00"), nil, action(exec, "echo('Exit configuring mode');")).
transition(s31, active_exit, nil, nil, action(exec, "beep();")).
transition(reading, s71, event(call, set), nil, action(log, "ABORT 'Slow blinking red LED'")).
transition(s71, configuring, nil, nil, action(exec, "echo('Configuring mode');")).
transition(reading, s91, event(when, "tCurrent >= tThreshold"), nil, action(log, "ABORT 'Slow blinking red LED'")).
transition(configuring, configuring, event(set, tThreshold), nil, action(exec, "doubleBeep();")).
transition(configuring, configuring, event(call, done), "tThreshold <= tCurrent", action(exec, "generateError();")).