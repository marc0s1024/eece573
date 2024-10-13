module tb_pointer_sync;
    parameter SIZE = 4; 
    logic clk;
    logic [SIZE-1:0] bin_ptr_in, sync_gray_ptr_out;

    // inst pointer_sync
    pointer_sync #(.SIZE(SIZE)) pointer_sync_inst (
        .clk(clk),
        .bin_ptr_in(bin_ptr_in),
        .sync_gray_ptr_out(sync_gray_ptr_out)
    );

    // gen clk
    initial clk = 0;
    always #5 clk = ~clk; // toggle clk every 5 time units

    // test
    initial begin
        bin_ptr_in = 4'b0000; // input
        #10; // delay 10 time units
        bin_ptr_in = 4'b0001;
        #10;
        bin_ptr_in = 4'b0010;
        #10;
        bin_ptr_in = 4'b0011;
        #10;
        bin_ptr_in = 4'b0100;
        #10;
        bin_ptr_in = 4'b0101;
        #10;
        bin_ptr_in = 4'b0110;
        #10;
        bin_ptr_in = 4'b0111;
        #10;
        bin_ptr_in = 4'b1000;
        #10;
        bin_ptr_in = 4'b1001;
        #10;
        bin_ptr_in = 4'b1010;
        #10;
        bin_ptr_in = 4'b1011;
        #10;
        bin_ptr_in = 4'b1100;
        #10;
        bin_ptr_in = 4'b1101;
        #10;
        bin_ptr_in = 4'b1110;
        #10;
        bin_ptr_in = 4'b1111;
        #10;
        $finish;
    end