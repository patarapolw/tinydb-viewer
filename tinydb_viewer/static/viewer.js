var container = document.getElementById('hotArea');
var actualConfig = {
    undo: true,
    modifyColWidth: function(width, col){
        if(width > maxColWidth) return maxColWidth;
    },
    contextMenu: [
        // 'row_above', 'row_below', 
        'remove_row'
    ],
    afterChange: (changes, source)=>{
        if([
            'edit', 
            'Autofill.fill', 
            'CopyPaste.paste', 
            'UndoRedo.redo', 'UndoRedo.undo'
        ].indexOf(source) !== -1){
            for(let change of changes){
                if(change[2] !== change[3]){
                    fetch('api/edit', {
                        method: 'POST',
                        headers: {
                            "Content-Type": "application/json; charset=utf-8"
                        },
                        body: JSON.stringify({
                            id: hot.getRowHeader(change[0]),
                            fieldName: change[1],
                            data: change[3],
                            table: table
                        })
                    }).then(r=>{
                        if(r.status === 201){
                            r.json()
                        } else {
                            throw 'Request failed.';
                        }
                    }).then(rj=>{
                        alert(rj.record + 'edited');
                    }).catch(e=>{
                        alert(e);
                        hot.setDataAtCell([
                            [change[0], change[1], change[2]]
                        ])
                    })
                }
            }
        }
    },
    beforeRemoveRow: (index, amount, physicalRows)=>{
        if(confirm('Are you sure you want ot remove ' + hot.getDataAtRow(index) + '?')){
            fetch('api/delete/' + table + '/'+ index, {
                method: 'DELETE'
            }).then(r=>{
                if(r.status === 303){
                    r.json();
                }
            }).then(rj=>{
                alert(rj.record + 'deleted');
            }).catch(e=>console.error(e));
        } else {
            return false;
        }
    }
}
config = Object.assign(actualConfig, config);
var hot = new Handsontable(container, config);

colWidths = [];
[...Array(hot.countCols()).keys()].map(i => {
    colWidths.push(hot.getColWidth(i));
});

hot.updateSettings({
    colWidths: colWidths
});

hot.updateSettings({
    modifyColWidth: ()=>{}
});
