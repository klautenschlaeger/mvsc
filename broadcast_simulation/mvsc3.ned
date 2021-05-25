simple MvSc_node
{
    parameters:
        int id = default(1);
        @display("i=block/routing");
    gates:
        inout gate[];
}

network mvsc_network2
{
    @display("bgb=467,481");
    types:
        channel Channel extends ned.DelayChannel
        {
            delay = 250ms;
        }
    submodules:
        l1: MvSc_node {
            parameters:
                id = 1;
                @display("p=179,104");
        }
        l2: MvSc_node {
            parameters:
                id = 2;
                @display("p=53,218"); // do not change the icon (first arg of i=) just colorize it
        }
    connections:
        l1.gate++ <--> Channel <--> l2.gate++;
}

network mvsc_network3
{
    @display("bgb=467,481");
    types:
        channel Channel extends ned.DelayChannel
        {
            delay = 250ms;
        }
    submodules:
        l1: MvSc_node {
            parameters:
                id = 1;
                @display("p=179,104");
        }
        l2: MvSc_node {
            parameters:
                id = 2;
                @display("p=53,218"); // do not change the icon (first arg of i=) just colorize it
        }
        l3: MvSc_node {
            parameters:
                id = 3;
                @display("p=246,259"); // here too
        }
    connections:
        l3.gate++ <--> Channel <--> l1.gate++;
        l3.gate++ <--> Channel <--> l2.gate++;
        l1.gate++ <--> Channel <--> l2.gate++;
}

network mvsc_network4
{
    @display("bgb=467,481");
    types:
        channel Channel extends ned.DelayChannel
        {
            delay = 250ms;
        }
    submodules:
        l1: MvSc_node {
            parameters:
                id = 1;
                @display("p=179,104");
        }
        l2: MvSc_node {
            parameters:
                id = 2;
                @display("p=53,218"); // do not change the icon (first arg of i=) just colorize it
        }
        l3: MvSc_node {
            parameters:
                id = 3;
                @display("p=246,259"); // here too
        }
        l4: MvSc_node {
            parameters:
                id = 4;
                @display("p=330,156"); // here too
        }
    connections:
        l3.gate++ <--> Channel <--> l1.gate++;
        l3.gate++ <--> Channel <--> l2.gate++;
        l1.gate++ <--> Channel <--> l2.gate++;
        l4.gate++ <--> Channel <--> l2.gate++;
        l4.gate++ <--> Channel <--> l1.gate++;
        l4.gate++ <--> Channel <--> l3.gate++;
}

network mvsc_network5
{
    @display("bgb=467,481");
    types:
        channel Channel extends ned.DelayChannel
        {
            delay = 250ms;
        }
    submodules:
        l1: MvSc_node {
            parameters:
                id = 1;
                @display("p=135,92");
        }
        l2: MvSc_node {
            parameters:
                id = 2;
                @display("p=53,218"); // do not change the icon (first arg of i=) just colorize it
        }
        l3: MvSc_node {
            parameters:
                id = 3;
                @display("p=233,288"); // here too
        }
        l4: MvSc_node {
            parameters:
                id = 4;
                @display("p=372,170"); // here too
        }
        l5: MvSc_node {
            parameters:
                id = 5;
                @display("p=305,78"); // here too
        }
    connections:
        l3.gate++ <--> Channel <--> l1.gate++;
        l3.gate++ <--> Channel <--> l2.gate++;
        l1.gate++ <--> Channel <--> l2.gate++;
        l4.gate++ <--> Channel <--> l2.gate++;
        l4.gate++ <--> Channel <--> l1.gate++;
        l4.gate++ <--> Channel <--> l3.gate++;
        l5.gate++ <--> Channel <--> l2.gate++;
        l5.gate++ <--> Channel <--> l1.gate++;
        l5.gate++ <--> Channel <--> l3.gate++;
        l5.gate++ <--> Channel <--> l4.gate++;
}

network mvsc_network6
{
    @display("bgb=467,481");
    types:
        channel Channel extends ned.DelayChannel
        {
            delay = 250ms;
        }
    submodules:
        l1: MvSc_node {
            parameters:
                id = 1;
                @display("p=145,64");
        }
        l2: MvSc_node {
            parameters:
                id = 2;
                @display("p=64,164"); // do not change the icon (first arg of i=) just colorize it
        }
        l3: MvSc_node {
            parameters:
                id = 3;
                @display("p=141,260"); // here too
        }
        l4: MvSc_node {
            parameters:
                id = 4;
                @display("p=281,269"); // here too
        }
        l5: MvSc_node {
            parameters:
                id = 5;
                @display("p=370,171"); // here too
        }
        l6: MvSc_node {
            parameters:
                id = 6;
                @display("p=281,69"); // here too
        }
    connections:
        l3.gate++ <--> Channel <--> l1.gate++;
        l3.gate++ <--> Channel <--> l2.gate++;
        l1.gate++ <--> Channel <--> l2.gate++;
        l4.gate++ <--> Channel <--> l2.gate++;
        l4.gate++ <--> Channel <--> l1.gate++;
        l4.gate++ <--> Channel <--> l3.gate++;
        l5.gate++ <--> Channel <--> l2.gate++;
        l5.gate++ <--> Channel <--> l1.gate++;
        l5.gate++ <--> Channel <--> l3.gate++;
        l5.gate++ <--> Channel <--> l4.gate++;
        l6.gate++ <--> Channel <--> l2.gate++;
        l6.gate++ <--> Channel <--> l1.gate++;
        l6.gate++ <--> Channel <--> l3.gate++;
        l6.gate++ <--> Channel <--> l4.gate++;
        l6.gate++ <--> Channel <--> l5.gate++;
}

network mvsc_network7
{
    @display("bgb=467,481");
    types:
        channel Channel extends ned.DelayChannel
        {
            delay = 250ms;
        }
    submodules:
        l1: MvSc_node {
            parameters:
                id = 1;
                @display("p=130,64");
        }
        l2: MvSc_node {
            parameters:
                id = 2;
                @display("p=77,154"); // do not change the icon (first arg of i=) just colorize it
        }
        l3: MvSc_node {
            parameters:
                id = 3;
                @display("p=127,286"); // here too
        }
        l4: MvSc_node {
            parameters:
                id = 4;
                @display("p=240,325"); // here too
        }
        l5: MvSc_node {
            parameters:
                id = 5;
                @display("p=359,291"); // here too
        }
        l6: MvSc_node {
            parameters:
                id = 6;
                @display("p=423,156"); // here too
        }
        l7: MvSc_node {
            parameters:
                id = 7;
                @display("p=364,70"); // here too
        }
    connections:
        l3.gate++ <--> Channel <--> l1.gate++;
        l3.gate++ <--> Channel <--> l2.gate++;
        l1.gate++ <--> Channel <--> l2.gate++;
        l4.gate++ <--> Channel <--> l2.gate++;
        l4.gate++ <--> Channel <--> l1.gate++;
        l4.gate++ <--> Channel <--> l3.gate++;
        l5.gate++ <--> Channel <--> l2.gate++;
        l5.gate++ <--> Channel <--> l1.gate++;
        l5.gate++ <--> Channel <--> l3.gate++;
        l5.gate++ <--> Channel <--> l4.gate++;
        l6.gate++ <--> Channel <--> l2.gate++;
        l6.gate++ <--> Channel <--> l1.gate++;
        l6.gate++ <--> Channel <--> l3.gate++;
        l6.gate++ <--> Channel <--> l4.gate++;
        l6.gate++ <--> Channel <--> l5.gate++;
        l7.gate++ <--> Channel <--> l2.gate++;
        l7.gate++ <--> Channel <--> l1.gate++;
        l7.gate++ <--> Channel <--> l3.gate++;
        l7.gate++ <--> Channel <--> l4.gate++;
        l7.gate++ <--> Channel <--> l5.gate++;
        l7.gate++ <--> Channel <--> l6.gate++;
}
network mvsc_network8
{
    @display("bgb=467,481");
    types:
        channel Channel extends ned.DelayChannel
        {
            delay = 250ms;
        }
    submodules:
        l1: MvSc_node {
            parameters:
                id = 1;
                @display("p=151,109");
        }
        l2: MvSc_node {
            parameters:
                id = 2;
                @display("p=49,189"); // do not change the icon (first arg of i=) just colorize it
        }
        l3: MvSc_node {
            parameters:
                id = 3;
                @display("p=45,327"); // here too
        }
        l4: MvSc_node {
            parameters:
                id = 4;
                @display("p=141,416"); // here too
        }
        l5: MvSc_node {
            parameters:
                id = 5;
                @display("p=286,420"); // here too
        }
        l6: MvSc_node {
            parameters:
                id = 6;
                @display("p=395,334"); // here too
        }
        l7: MvSc_node {
            parameters:
                id = 7;
                @display("p=395,185"); // here too
        }
        l8: MvSc_node {
            parameters:
                id = 8;
                @display("p=289,111"); // here too
        }
    connections:
        l3.gate++ <--> Channel <--> l1.gate++;
        l3.gate++ <--> Channel <--> l2.gate++;
        l1.gate++ <--> Channel <--> l2.gate++;
        l4.gate++ <--> Channel <--> l2.gate++;
        l4.gate++ <--> Channel <--> l1.gate++;
        l4.gate++ <--> Channel <--> l3.gate++;
        l5.gate++ <--> Channel <--> l2.gate++;
        l5.gate++ <--> Channel <--> l1.gate++;
        l5.gate++ <--> Channel <--> l3.gate++;
        l5.gate++ <--> Channel <--> l4.gate++;
        l6.gate++ <--> Channel <--> l2.gate++;
        l6.gate++ <--> Channel <--> l1.gate++;
        l6.gate++ <--> Channel <--> l3.gate++;
        l6.gate++ <--> Channel <--> l4.gate++;
        l6.gate++ <--> Channel <--> l5.gate++;
        l7.gate++ <--> Channel <--> l2.gate++;
        l7.gate++ <--> Channel <--> l1.gate++;
        l7.gate++ <--> Channel <--> l3.gate++;
        l7.gate++ <--> Channel <--> l4.gate++;
        l7.gate++ <--> Channel <--> l5.gate++;
        l7.gate++ <--> Channel <--> l6.gate++;
        l8.gate++ <--> Channel <--> l2.gate++;
        l8.gate++ <--> Channel <--> l1.gate++;
        l8.gate++ <--> Channel <--> l3.gate++;
        l8.gate++ <--> Channel <--> l4.gate++;
        l8.gate++ <--> Channel <--> l5.gate++;
        l8.gate++ <--> Channel <--> l6.gate++;
        l8.gate++ <--> Channel <--> l7.gate++;
}

network mvsc_network9
{
    @display("bgb=467,481");
    types:
        channel Channel extends ned.DelayChannel
        {
            delay = 250ms;
        }
    submodules:
        l1: MvSc_node {
            parameters:
                id = 1;
                @display("p=145,85");
        }
        l2: MvSc_node {
            parameters:
                id = 2;
                @display("p=65,171"); // do not change the icon (first arg of i=) just colorize it
        }
        l3: MvSc_node {
            parameters:
                id = 3;
                @display("p=66,294"); // here too
        }
        l4: MvSc_node {
            parameters:
                id = 4;
                @display("p=146,382"); // here too
        }
        l5: MvSc_node {
            parameters:
                id = 5;
                @display("p=244,429"); // here too
        }
        l6: MvSc_node {
            parameters:
                id = 6;
                @display("p=312,388"); // here too
        }
        l7: MvSc_node {
            parameters:
                id = 7;
                @display("p=378,295"); // here too
        }
        l8: MvSc_node {
            parameters:
                id = 8;
                @display("p=377,178"); // here too
        }
        l9: MvSc_node {
            parameters:
                id = 9;
                @display("p=310,86"); // here too
        }
    connections:
        l3.gate++ <--> Channel <--> l1.gate++;
        l3.gate++ <--> Channel <--> l2.gate++;
        l1.gate++ <--> Channel <--> l2.gate++;
        l4.gate++ <--> Channel <--> l2.gate++;
        l4.gate++ <--> Channel <--> l1.gate++;
        l4.gate++ <--> Channel <--> l3.gate++;
        l5.gate++ <--> Channel <--> l2.gate++;
        l5.gate++ <--> Channel <--> l1.gate++;
        l5.gate++ <--> Channel <--> l3.gate++;
        l5.gate++ <--> Channel <--> l4.gate++;
        l6.gate++ <--> Channel <--> l2.gate++;
        l6.gate++ <--> Channel <--> l1.gate++;
        l6.gate++ <--> Channel <--> l3.gate++;
        l6.gate++ <--> Channel <--> l4.gate++;
        l6.gate++ <--> Channel <--> l5.gate++;
        l7.gate++ <--> Channel <--> l2.gate++;
        l7.gate++ <--> Channel <--> l1.gate++;
        l7.gate++ <--> Channel <--> l3.gate++;
        l7.gate++ <--> Channel <--> l4.gate++;
        l7.gate++ <--> Channel <--> l5.gate++;
        l7.gate++ <--> Channel <--> l6.gate++;
        l8.gate++ <--> Channel <--> l2.gate++;
        l8.gate++ <--> Channel <--> l1.gate++;
        l8.gate++ <--> Channel <--> l3.gate++;
        l8.gate++ <--> Channel <--> l4.gate++;
        l8.gate++ <--> Channel <--> l5.gate++;
        l8.gate++ <--> Channel <--> l6.gate++;
        l8.gate++ <--> Channel <--> l7.gate++;
        l9.gate++ <--> Channel <--> l2.gate++;
        l9.gate++ <--> Channel <--> l1.gate++;
        l9.gate++ <--> Channel <--> l3.gate++;
        l9.gate++ <--> Channel <--> l4.gate++;
        l9.gate++ <--> Channel <--> l5.gate++;
        l9.gate++ <--> Channel <--> l6.gate++;
        l9.gate++ <--> Channel <--> l7.gate++;
        l9.gate++ <--> Channel <--> l8.gate++;
}

network mvsc_network10
{
    @display("bgb=467,481");
    types:
        channel Channel extends ned.DelayChannel
        {
            delay = 250ms;
        }
    submodules:
        l1: MvSc_node {
            parameters:
                id = 1;
                @display("p=110,112");
        }
        l2: MvSc_node {
            parameters:
                id = 2;
                @display("p=43,208"); // do not change the icon (first arg of i=) just colorize it
        }
        l3: MvSc_node {
            parameters:
                id = 3;
                @display("p=44,317"); // here too
        }
        l4: MvSc_node {
            parameters:
                id = 4;
                @display("p=109,417"); // here too
        }
        l5: MvSc_node {
            parameters:
                id = 5;
                @display("p=241,450"); // here too
        }
        l6: MvSc_node {
            parameters:
                id = 6;
                @display("p=380,415"); // here too
        }
        l7: MvSc_node {
            parameters:
                id = 7;
                @display("p=435,318"); // here too
        }
        l8: MvSc_node {
            parameters:
                id = 8;
                @display("p=435,211"); // here too
        }
        l9: MvSc_node {
            parameters:
                id = 9;
                @display("p=370,116"); // here too
        }
        l10: MvSc_node {
            parameters:
                id = 10;
                @display("p=237,85"); // here too
        }
    connections:
        l3.gate++ <--> Channel <--> l1.gate++;
        l3.gate++ <--> Channel <--> l2.gate++;
        l1.gate++ <--> Channel <--> l2.gate++;
        l4.gate++ <--> Channel <--> l2.gate++;
        l4.gate++ <--> Channel <--> l1.gate++;
        l4.gate++ <--> Channel <--> l3.gate++;
        l5.gate++ <--> Channel <--> l2.gate++;
        l5.gate++ <--> Channel <--> l1.gate++;
        l5.gate++ <--> Channel <--> l3.gate++;
        l5.gate++ <--> Channel <--> l4.gate++;
        l6.gate++ <--> Channel <--> l2.gate++;
        l6.gate++ <--> Channel <--> l1.gate++;
        l6.gate++ <--> Channel <--> l3.gate++;
        l6.gate++ <--> Channel <--> l4.gate++;
        l6.gate++ <--> Channel <--> l5.gate++;
        l7.gate++ <--> Channel <--> l2.gate++;
        l7.gate++ <--> Channel <--> l1.gate++;
        l7.gate++ <--> Channel <--> l3.gate++;
        l7.gate++ <--> Channel <--> l4.gate++;
        l7.gate++ <--> Channel <--> l5.gate++;
        l7.gate++ <--> Channel <--> l6.gate++;
        l8.gate++ <--> Channel <--> l2.gate++;
        l8.gate++ <--> Channel <--> l1.gate++;
        l8.gate++ <--> Channel <--> l3.gate++;
        l8.gate++ <--> Channel <--> l4.gate++;
        l8.gate++ <--> Channel <--> l5.gate++;
        l8.gate++ <--> Channel <--> l6.gate++;
        l8.gate++ <--> Channel <--> l7.gate++;
        l9.gate++ <--> Channel <--> l2.gate++;
        l9.gate++ <--> Channel <--> l1.gate++;
        l9.gate++ <--> Channel <--> l3.gate++;
        l9.gate++ <--> Channel <--> l4.gate++;
        l9.gate++ <--> Channel <--> l5.gate++;
        l9.gate++ <--> Channel <--> l6.gate++;
        l9.gate++ <--> Channel <--> l7.gate++;
        l9.gate++ <--> Channel <--> l8.gate++;
        l10.gate++ <--> Channel <--> l2.gate++;
        l10.gate++ <--> Channel <--> l1.gate++;
        l10.gate++ <--> Channel <--> l3.gate++;
        l10.gate++ <--> Channel <--> l4.gate++;
        l10.gate++ <--> Channel <--> l5.gate++;
        l10.gate++ <--> Channel <--> l6.gate++;
        l10.gate++ <--> Channel <--> l7.gate++;
        l10.gate++ <--> Channel <--> l8.gate++;
        l10.gate++ <--> Channel <--> l9.gate++;
}

