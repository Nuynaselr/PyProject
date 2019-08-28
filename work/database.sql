CREATE table monitoring_system(
  UID VARCHAR(10),
  PID INTEGER,
  PPID INTEGER,
  C INTEGER,
  SZ INTEGER,
  RSS INTEGER,
  PSR INTEGER,
  STIME VARCHAR(5),
  TTY VARCHAR(10),
  TIME VARCHAR(8),
  CMD VARCHAR(70),
  ENDTIME VARCHAR(8),
  PRIMARY KEY (PID)
);