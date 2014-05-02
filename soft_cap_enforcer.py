from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import *

# def printer(pkt):
#   print "Bytes: "
#   print len(pkt['raw'])

class soft_cap_enforcer(DynamicPolicy):
  def __init__(self):
    super(soft_cap_enforcer,self).__init__()

    # Initialize byte counters
    self.allowed_traffic = 0
    self.allowed = True;

    # Set the cap enforcement callback
    # Note: Handling every packet in the controller requires some pretty 
    #       significant CPU power; It'd be better if some of this policy's
    #       logic could be delegated to the router
    self.query = packets()
    self.query.register_callback(self.enforce_cap)

    # Start the thread that adds allowed_traffic
    import threading
    self.cap_thread = threading.Thread(target=self.cap_thread)
    self.cap_lock = threading.Lock()
    self.cap_thread.daemon = True
    self.cap_thread.start()

    # Default to allowing traffic
    self.policy = self.query + identity

  def enforce_cap(self,pkt):
    # Subtract the size of the current packet from available traffic
    # Note: I would've preferred to use the built-in count_bytes policies
    #       but I couldn't get them to stop returning 0 all the time
    self.cap_lock.acquire()
    self.allowed_traffic = self.allowed_traffic - len(pkt['raw']);

    # Figure out if we should drop or allow traffic
    if self.allowed_traffic > 0:
      self.cap_lock.release()
      if self.allowed == False:
        self.policy = self.query + identity
        self.allowed = True;
    else:
      self.cap_lock.release()
      if self.allowed == True:
        self.policy = self.query + drop
        self.allowed = False;


  def cap_thread(self):
    # Frequency of adding bytes
    update_interval = 1 #seconds

    # Calculate the amortized rate for adding credit that keeps us
    # below our cap
    monthly_cap = 300 #gigabytes
    daily_bytes = monthly_cap * 1000000000 / 31
    bytes_per_sec = daily_bytes / (60*60*24)

    # Start adding credit at the proper amortized rate
    while True:
      self.cap_lock.acquire()
      self.allowed_traffic = self.allowed_traffic + (bytes_per_sec * update_interval)
      print "Token bucket credit: %d bytes" % self.allowed_traffic
      self.cap_lock.release()
      time.sleep(update_interval)



def main():
  from pyretic.modules.mac_learner import mac_learner

  return soft_cap_enforcer() >> mac_learner()
  