module gray2bin #(parameter SIZE = 4) (
    input logic [SIZE-1:0] gray,
    output logic [SIZE-1:0] bin
);
    integer i;
    always_comb begin
        for (i = 0; i < SIZE; i = i + 1) begin
            bin[i] = ^(gray >> i);
        end
    end
endmodule