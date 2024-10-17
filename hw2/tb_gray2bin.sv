module tb_gray2bin;
    parameter SIZE = 4;
    logic [SIZE-1:0] gray_in, bin_out;

    // inst gray2bin
    gray2bin #(.SIZE(SIZE)) gray2bin_test  (
        .gray(gray_in),
        .bin(bin_out)
    );

    initial begin
        gray_in = 4'b0000; // input
        #1; // delay 1 ns
        gray_in = 4'b0001;
        #1;
        gray_in = 4'b0010;
        #1;
        gray_in = 4'b0011;
        #1;
        gray_in = 4'b0100;
        #1;
        gray_in = 4'b0101;
        #1;
        gray_in = 4'b0110;
        #1;
        gray_in = 4'b0111;
        #1;
        gray_in = 4'b1000;
        #1;
        gray_in = 4'b1001;
        #1;
        gray_in = 4'b1010;
        #1;
        gray_in = 4'b1011;
        #1;
        gray_in = 4'b1100;
        #1;
        gray_in = 4'b1101;
        #1;
        gray_in = 4'b1110;
        #1;
        gray_in = 4'b1111;
        #1;
    end
endmodule