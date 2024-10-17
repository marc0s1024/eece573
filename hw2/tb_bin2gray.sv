module tb_bin2gray;
    parameter SIZE = 4;
    logic [SIZE-1:0] bin_in, gray_out;

    // inst bin2gray
    bin2gray #(.SIZE(SIZE)) bin2gray_test  (
        .bin(bin_in),
        .gray(gray_out)
    );

    initial begin
        bin_in = 4'b0000; // input
        #1; // delay 1 ns
        bin_in = 4'b0001;
        #1;
        bin_in = 4'b0010;
        #1;
        bin_in = 4'b0011;
        #1;
        bin_in = 4'b0100;
        #1;
        bin_in = 4'b0101;
        #1;
        bin_in = 4'b0110;
        #1;
        bin_in = 4'b0111;
        #1;
        bin_in = 4'b1000;
        #1;
        bin_in = 4'b1001;
        #1;
        bin_in = 4'b1010;
        #1;
        bin_in = 4'b1011;
        #1;
        bin_in = 4'b1100;
        #1;
        bin_in = 4'b1101;
        #1;
        bin_in = 4'b1110;
        #1;
        bin_in = 4'b1111;
        #1;
    end
endmodule