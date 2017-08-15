X_out = [];
Y_out = [];
n=3 ; figure ; xlim([0,1]); ylim([0,1]) ; hold on ; offset = 0.05; %added
for i=1:n,
    [px py ] = ginput(1);
    X_out = [X_out ; px];
    Y_out = [Y_out ; py];
    plot( px, py, 'r+' );
    % text_handle = text( px+5, py, num2str(i) );
    text_handle = text( px+offset, py, num2str(i) ); % changed
    % set(text_handle,'Color',[1 1 1])
    set(text_handle,'Color',[0 0 0]) % changed
end