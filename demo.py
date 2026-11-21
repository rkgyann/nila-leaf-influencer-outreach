"""Offline demonstration. Uses a separate SQLite database and never connects or sends email."""
import os, tempfile, datetime as dt
from pathlib import Path
import app

def run():
 with tempfile.TemporaryDirectory(prefix='nila-demo-') as tmp:
  app.DB=Path(tmp)/'demo.db';c=app.conn()
  print('\n1. Import fictional CSV research; duplicates are ignored')
  app.import_csv(c,app.ROOT/'sample_data/influencers.csv');app.import_csv(c,app.ROOT/'sample_data/influencers.csv')
  print('\n2. MOCK scoring: no Claude request')
  for i in (1,2,3):app.analyze(c,i,True)
  print('\n3. MOCK initial draft (not sent)');app.create_draft(c,1,'initial',True)
  print('\n4. Simulate a send four days ago; detect follow-up due')
  c.execute("UPDATE leads SET status='Email Sent',last_sent=? WHERE id=1",((app.now()-dt.timedelta(days=4)).isoformat(),));c.commit();app.due(c)
  print('\n5. MOCK follow-up draft (not sent)');app.create_draft(c,1,'followup',True)
  print('\n6. Simulate a reply, classify it and create a reply draft')
  c.execute("UPDATE leads SET status='Replied',reply_text='I am interested. What are your rates?' WHERE id=1");c.commit();app.classify(c,1,True);app.create_draft(c,1,'reply',True)
  print('\n7. CRM result:',dict(app.lead(c,1)))
  print('\nOFFLINE SIMULATION ONLY: no Instagram lookup, Claude call, Gmail connection or email send occurred.')
  c.close()
if __name__=='__main__':run()
