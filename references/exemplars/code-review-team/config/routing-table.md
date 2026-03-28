# Routing Table

## File Pattern → Agent Mapping

| Pattern | Primary Agent | Reasoning |
|---------|--------------|-----------|
| auth*, login*, session*, token* | security-reviewer | Auth is security-critical |
| *.sql, *query*, *migration* | security-reviewer + performance-reviewer | Injection + N+1 risks |
| config*, env*, *.yaml, *.json | architecture-reviewer | Configuration decisions |
| route*, middleware*, api/* | architecture-reviewer + security-reviewer | Boundary + auth |
| *.test.*, *.spec.* | architecture-reviewer | Test architecture |
| component*, render*, page* | performance-reviewer | Render performance |
| *index*, *barrel*, *export* | architecture-reviewer | Module structure |
| * (default) | all three | Comprehensive review |
