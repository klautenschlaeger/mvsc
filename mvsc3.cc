#include <stdio.h>
#include <string.h>
#include <omnetpp.h>
#include <iostream>
#include <queue>

using namespace omnetpp;


#include <mvsc3_m.h>



class MessageMvSc {
  int time;
  int coord_cnt;
  int status;
  int id;
public:
  MessageMvSc(){}
  MessageMvSc(int time, int coord, int status, int id)
      {
          this->time = time;
          this->coord_cnt = coord;
          this->status = status;
          this->id = id;
      }
  void setTime(int i) { time = i; }
  int getTime() { return time; }
  void setCoord_cnt(int i) { coord_cnt = i; }
  int getCoord_cnt() { return coord_cnt; }
  void setStatus(int i) { status = i; }
  int getStatus() { return status; }
  void setId(int i) { id = i; }
  int getId() { return id; }
};

class Multipolygon {
  int interval;
  int coord_cnt;
public:
  Multipolygon(){}
  Multipolygon(int x, int y)
      {
          this->interval = x;
          this->coord_cnt = y;
      }
  void setInterval(int i) { interval = i; }
  int getInterval() { return interval; }
  void setCoord_cnt(int i) { coord_cnt = i; }
  int getCoord_cnt() { return coord_cnt; }
};
class MvSc_node : public cSimpleModule
{
  private:
    cMessage *event;  // pointer to the event object which we'll use for timing
    cMessage *sending;
    cMessage *measure;
    Multipolygon multipolys[581];
    cOutVector measureVector;
    int intervals[581] = {74, 73, 19, 2, 3, 74, 15, 3, 3, 1, 5, 1, 9, 0, 2, 1, 1, 70, 72, 70, 2, 3, 2, 1, 11, 0, 2, 71, 67, 69, 68, 68, 68, 69, 68, 67, 68, 63, 63, 68, 54, 1, 2, 1, 1, 4, 1, 0, 9, 1, 1, 0, 39, 68, 69, 68, 68, 2, 1, 2, 2, 4, 0, 1, 27, 2, 56, 18, 2, 27, 0, 1, 2, 1, 6, 0, 1, 1, 61, 60, 65, 63, 65, 5, 1, 0, 2, 2, 2, 4, 0, 65, 56, 18, 2, 3, 9, 45, 56, 57, 57, 57, 63, 66, 66, 65, 54, 11, 3, 1, 3, 4, 3, 1, 2, 35, 39, 3, 1, 41, 64, 48, 69, 68, 60, 1, 65, 64, 58, 1, 1, 6, 4, 1, 4, 49, 41, 4, 8, 66, 67, 27, 67, 67, 63, 16, 68, 65, 63, 66, 65, 33, 0, 35, 67, 67, 68, 67, 68, 3, 1, 67, 66, 68, 66, 65, 43, 46, 67, 64, 68, 68, 69, 4, 69, 69, 69, 69, 69, 57, 1, 2, 27, 68, 67, 71, 61, 57, 32, 59, 56, 56, 58, 55, 57, 2, 4, 36, 58, 57, 58, 57, 58, 28, 58, 57, 57, 57, 58, 57, 11, 2, 11, 57, 55, 55, 54, 56, 56, 5, 55, 55, 54, 57, 55, 56, 21, 42, 57, 56, 52, 57, 57, 40, 56, 55, 55, 54, 54, 54, 30, 5, 35, 54, 53, 54, 53, 54, 53, 54, 54, 52, 52, 52, 52, 38, 1, 3, 9, 56, 12, 0, 53, 54, 53, 54, 53, 26, 4, 58, 55, 54, 55, 54, 55, 48, 1, 7, 57, 56, 57, 56, 57, 56, 50, 53, 54, 54, 54, 54, 54, 55, 7, 0, 7, 54, 55, 54, 55, 55, 54, 55, 8, 54, 55, 54, 54, 55, 54, 54, 20, 1, 7, 55, 55, 55, 55, 54, 56, 56, 21, 56, 56, 56, 56, 55, 56, 56, 34, 2, 7, 57, 56, 57, 57, 57, 57, 57, 38, 58, 57, 58, 57, 57, 58, 57, 50, 1, 0, 7, 58, 58, 58, 58, 57, 58, 58, 52, 55, 53, 54, 54, 54, 54, 54, 54, 7, 7, 56, 57, 57, 57, 57, 57, 57, 57, 7, 57, 57, 57, 57, 57, 57, 57, 56, 20, 2, 7, 57, 56, 57, 56, 57, 57, 57, 57, 23, 57, 57, 58, 57, 58, 57, 51, 56, 40, 2, 4, 32, 55, 55, 56, 55, 55, 56, 55, 55, 7, 56, 55, 55, 56, 56, 56, 7, 58, 55, 40, 0, 1, 56, 55, 56, 55, 54, 55, 56, 55, 48, 56, 56, 55, 55, 56, 55, 56, 55, 43, 6, 2, 0, 11, 55, 55, 55, 56, 55, 55, 56, 54, 41, 55, 56, 60, 67, 66, 61, 63, 67, 63, 4, 48, 65, 64, 65, 62, 59, 62, 62, 62, 21, 64, 66, 60, 66, 63, 65, 68, 67, 67, 15, 65, 63, 62, 62, 63, 62, 63, 63, 58, 15, 54, 54, 53, 54, 47, 45, 15, 26, 53, 53, 53, 53, 52, 53, 52, 53, 52, 20, 53, 53, 54, 53, 52, 52, 53, 53, 54, 22, 1, 47, 49, 52, 18, 2, 2, 57, 55, 56, 27, 1, 53, 50, 50, 19, 1, 15, 53, 52, 22, 56, 55, 16, 1, 5, 7, 1, 14, 63, 51, 61, 43, 2, 0, 2, 3, 15, 61, 20, 62, 12, 1, 9, 12, 48, 38, 4, 0, 4, 4, 26};
    int coord_cnts[581] = {47, 43, 16, 30, 10, 46, 27, 9, 25, 8, 14, 5, 46, 5, 10, 5, 9, 46, 36, 38, 27, 9, 17, 5, 41, 5, 5, 54, 25, 29, 35, 44, 39, 49, 36, 31, 34, 33, 31, 31, 40, 11, 16, 6, 5, 20, 5, 5, 40, 8, 6, 5, 38, 51, 51, 42, 42, 8, 7, 17, 21, 27, 5, 5, 25, 27, 49, 20, 25, 37, 5, 5, 14, 18, 34, 5, 5, 5, 45, 29, 35, 32, 37, 9, 5, 5, 11, 12, 26, 21, 5, 42, 38, 24, 10, 13, 30, 31, 31, 30, 39, 39, 30, 44, 35, 37, 41, 15, 7, 5, 5, 5, 5, 5, 13, 61, 52, 5, 5, 61, 54, 56, 55, 29, 60, 9, 36, 26, 57, 5, 5, 7, 5, 5, 5, 62, 59, 53, 57, 39, 62, 48, 44, 33, 25, 29, 36, 29, 39, 40, 31, 54, 22, 61, 32, 28, 33, 35, 30, 9, 5, 31, 39, 44, 36, 22, 73, 60, 45, 29, 42, 40, 32, 13, 43, 28, 31, 32, 37, 53, 25, 9, 61, 33, 29, 32, 28, 23, 24, 37, 41, 21, 25, 33, 41, 33, 14, 61, 29, 25, 31, 19, 31, 18, 27, 27, 23, 21, 25, 22, 50, 14, 61, 35, 21, 25, 24, 23, 27, 9, 35, 31, 34, 33, 35, 31, 64, 60, 35, 29, 23, 31, 36, 31, 28, 27, 33, 29, 19, 24, 74, 10, 63, 36, 27, 43, 40, 49, 38, 27, 37, 31, 22, 27, 25, 52, 29, 11, 62, 37, 9, 5, 38, 29, 33, 32, 28, 19, 11, 38, 28, 29, 34, 22, 35, 58, 19, 52, 39, 32, 27, 32, 34, 23, 33, 29, 27, 25, 30, 27, 25, 25, 50, 23, 58, 29, 35, 31, 29, 21, 26, 30, 15, 32, 27, 32, 21, 32, 29, 33, 52, 33, 60, 28, 29, 32, 17, 32, 43, 33, 19, 35, 23, 17, 23, 24, 29, 27, 57, 35, 57, 55, 21, 24, 19, 27, 23, 23, 27, 30, 23, 21, 23, 11, 27, 24, 60, 32, 7, 55, 33, 27, 25, 19, 35, 28, 31, 23, 35, 31, 23, 25, 29, 26, 32, 49, 65, 58, 41, 29, 24, 36, 21, 23, 27, 33, 19, 25, 29, 26, 29, 25, 19, 33, 28, 57, 35, 56, 41, 36, 29, 35, 31, 29, 23, 30, 16, 34, 32, 30, 27, 28, 32, 27, 34, 52, 39, 10, 61, 27, 27, 27, 35, 31, 32, 32, 28, 17, 38, 30, 16, 23, 31, 30, 12, 53, 37, 52, 25, 5, 59, 23, 21, 28, 21, 17, 27, 24, 31, 21, 19, 25, 32, 30, 27, 20, 29, 23, 28, 16, 8, 61, 35, 21, 22, 22, 25, 28, 23, 24, 19, 24, 24, 27, 31, 37, 32, 22, 29, 27, 45, 61, 28, 27, 24, 33, 31, 33, 29, 30, 10, 32, 29, 19, 19, 27, 34, 35, 19, 26, 58, 59, 35, 29, 27, 29, 27, 26, 30, 28, 17, 29, 19, 27, 32, 22, 19, 15, 48, 62, 30, 21, 27, 23, 23, 23, 24, 22, 13, 21, 23, 24, 33, 59, 30, 21, 26, 37, 46, 7, 40, 38, 49, 37, 9, 16, 61, 34, 19, 15, 9, 30, 30, 45, 24, 7, 60, 36, 27, 14, 25, 29, 66, 23, 7, 15, 12, 61, 48, 19, 33, 59, 28, 20, 11, 11, 60, 43, 9, 35, 48, 30, 20, 59, 39, 60, 31, 18, 7, 9, 47};
    int message_cnt;
    int coord_int = 0;
    int poly;
    int id;
    long numSent;
    long numReceived;
    long numReceivedOld;
    std::queue<MessageMvSc> newqueue;
  public:
    MvSc_node();
    virtual ~MvSc_node();
  protected:
    virtual MvScMsg *generateMessage(int status);
    virtual void forwardMessage(MvScMsg *msg, int time);
    virtual int calculateTime(int coord);
    virtual void refreshDisplay() const override;
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
};

Define_Module(MvSc_node);

MvSc_node::MvSc_node()
{
    // Set the pointer to nullptr, so that the destructor won't crash
    // even if initialize() doesn't get called because of a runtime
    // error or user cancellation during the startup process.
    event = nullptr;
    sending = nullptr;
    measure = nullptr;
}

MvSc_node::~MvSc_node()
{
    // Dispose of dynamically allocated the objects
    cancelAndDelete(event);
    cancelAndDelete(sending);
    cancelAndDelete(measure);
}

void MvSc_node::initialize()
{
    id = par("id");
    // Initialize variables
    numSent = 0;
    poly = 0;
    numReceived = 0;
    numReceivedOld = 0;
    message_cnt = 1000;
    WATCH(message_cnt);
    WATCH(numSent);
    WATCH(poly);
    WATCH(numReceived);
    WATCH(numReceivedOld);
    for (int i = 0; i < 581; ++i){
        multipolys[i] = Multipolygon(intervals[i], coord_cnts[i]);
    }
    measureVector.setName("Measurement");
    event = new cMessage("event");
    Multipolygon multi = multipolys[intuniform(0, 580)];
    coord_int = multi.getCoord_cnt();
    EV << multi.getInterval() << &endl;
    scheduleAt(simTime() + multi.getInterval(), event);
    sending = new cMessage("sending");
    scheduleAt(simTime() + id, sending);
    measure = new cMessage("measure");
    scheduleAt(simTime(), measure);

}

void MvSc_node::handleMessage(cMessage *msg)
{
    if (msg == event) {
            // The self-message arrived, so we can send out tictocMsg and nullptr out
            // its pointer so that it doesn't confuse us later.
            EV << "new poly arrived\n";

            delete msg;
            MessageMvSc message = MessageMvSc(calculateTime(coord_int), coord_int, 0, id);
            newqueue.push(message);
            poly++;
            event = new cMessage("event");
            Multipolygon multi = multipolys[intuniform(0, 580)];
            coord_int = multi.getCoord_cnt();
            scheduleAt(simTime() + multi.getInterval(), event);
    }
    else if (msg == measure){
        measureVector.recordWithTimestamp(simTime(), numSent);
        measureVector.recordWithTimestamp(simTime(), numReceived);
        measureVector.recordWithTimestamp(simTime(), numReceivedOld);
        measure = new cMessage("measure");
        scheduleAt(simTime() + 120.0, measure);
    }
    else if (msg == sending) {
            delete msg;
            if(message_cnt == 1000){
                EV << "LoRa time slot";
            }
            MessageMvSc message = MessageMvSc(0,0,0,0);
            if (!newqueue.empty()) {
                message = newqueue.front();
                newqueue.pop();
            }

            int time = message.getTime();
            sending = new cMessage("sending");
            if (message_cnt > time and time > 0){
                MvScMsg *msg = generateMessage(message.getStatus());
                forwardMessage(msg, time);
                numSent++;
                message_cnt = message_cnt - time;
                double d_time = time / 1000.0;
                scheduleAt(simTime() + d_time, sending);
            }
            else {
                Multipolygon multi = multipolys[intuniform(0, 580)];
                time = calculateTime(multi.getCoord_cnt());
                EV << "Time: " << time << "\n";
                if (message_cnt > time) {
                    message.setStatus(1);
                    message.setCoord_cnt(multi.getCoord_cnt());
                    message.setId(id);
                    message.setTime(time);
                    MvScMsg *msg = generateMessage(message.getStatus());
                    forwardMessage(msg, time);
                    numSent++;
                    message_cnt = message_cnt - time;
                    double d_time = time / 1000.0;
                    scheduleAt(simTime() + d_time, sending);
                }
                else{
                    double d_time = 9.0 + message_cnt / 1000.0;
                    EV << "D_Time: " << d_time << "  message_cnt: " << message_cnt <<"\n";
                    scheduleAt(simTime() + d_time, sending);
                    message_cnt = 1000;
                }

            }
    }
    else {
        MvScMsg *ttmsg = check_and_cast<MvScMsg *>(msg);

        if (ttmsg->getStatus() == 0) {
            // Message arrived.
            EV << "Message " << ttmsg << " arrived! \n";
            numReceived++;
        }
        if (ttmsg->getStatus() == 1) {
            // Message arrived.
            EV << "old Message " << ttmsg << " arrived! \n";
            numReceivedOld++;
        }
        delete ttmsg;
    }

}

MvScMsg *MvSc_node::generateMessage(int status)
{
    // Produce source and destination addresses.
    int src = id;
    char msgname[20];
    sprintf(msgname, "from-%d-status-%d", src, status);

    // Create message object and set source and destination field.
    MvScMsg *msg = new MvScMsg(msgname);
    msg->setSource(src);
    msg->setStatus(status);
    return msg;
}

int MvSc_node::calculateTime(int coord)
{
    int packet_size = 0;
    float time = 0.0;
    int sending_time = 0;
    if (coord <= 30){
        packet_size = (coord*8 + 8 + 2 + 1)*8;
        time = (packet_size / 10937.5) * 1000.0 + 20.0;
        sending_time = ceil(time);
        return sending_time;
    }
    else if (coord <= 60){
        packet_size = (30*8 + 8 + 2 + 1)*8;
        time = (packet_size / 10937.5) * 1000.0 + 20.0;
        sending_time = ceil(time);

        coord = coord - 30;
        packet_size = (coord*8 + 8 + 2 + 1)*8;
        time = (packet_size / 10937.5) * 1000.0 + 20.0;
        sending_time = sending_time + ceil(time);
        return sending_time;
    }
    else if (coord < 90){
        packet_size = (30*8 + 8 + 2 + 1)*8;
        time = (packet_size / 10937.5) * 1000.0 + 20.0;
        sending_time = ceil(time);

        packet_size = (30*8 + 8 + 2 + 1)*8;
        time = (packet_size / 10937.5) * 1000.0 + 20.0;
        sending_time = sending_time + ceil(time);
        coord = coord - 60;
        packet_size = (coord*8 + 8 + 2 + 1)*8;
        time = (packet_size / 10937.5) * 1000.0 + 20.0;
        sending_time = sending_time + ceil(time);
        return sending_time;
    }

}

void MvSc_node::forwardMessage(MvScMsg *msg, int time)
{
    // Increment hop count.

    // Same routing as before: random gate.
    double d_time = time/1000.0;
    int n = gateSize("gate");
    for (int i = 0; i < n; i++)
    {
        cGate *gOut = gate("gate$o", i);
        cChannel *channel = gOut->getChannel();
        cDelayChannel *dchannel = check_and_cast<cDelayChannel *>(channel);
        dchannel->setDelay(d_time);
        MvScMsg *copy = msg->dup();
        EV << "Forwarding message " << msg << " on gate[" << i << "]\n";
        send(copy, "gate$o", i);
    }
    delete msg;
}

void MvSc_node::refreshDisplay() const
{
    char buf[60];
    sprintf(buf, "rcvd new: %ld rcvd old: %ld sent: %ld", numReceived, numReceivedOld, numSent);
    getDisplayString().setTagArg("t", 0, buf);
}
