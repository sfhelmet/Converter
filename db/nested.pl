state(active).
superstate(active, reading).
superstate(reading, running).
superstate(reading, eating).
superstate(eating, drinking).
superstate(running, walking).
superstate(walking, jumping).
superstate(walking, crawling).
entry_pseudostate(active_skip_config_entry, reading).	% active superstate is implied
