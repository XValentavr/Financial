let comments = document.getElementById('setcomments')

function where_checker() {
    let search = document.getElementById('search').value
    let by_date = document.getElementById('by_date')
    let by_sum = document.getElementById('by_sum')
    let by_comm = document.getElementById('by_comment')
    if (search === 'По дате') {
        by_comm.style.display = 'none';
        by_sum.style.display = 'none';
        if (by_date.style.display === 'none') {
            by_date.style.display = 'block';
            comments.style.display = 'block'
        }

    } else if (search === 'По комментарию') {
        by_date.style.display = 'none';
        by_sum.style.display = 'none';
        if (by_comm.style.display === 'none') {
            by_comm.style.display = 'block';
            comments.style.display = 'block'
        }
    } else if (search === 'По сумме') {
        by_date.style.display = 'none';
        by_comm.style.display = 'none';
        if (by_comm.style.display === 'none') {
            by_sum.style.display = 'block';
            comments.style.display = 'block'
        }
        let summ_down = document.getElementById('search_sum').value
        if (summ_down === 'Точная сумма') {
            document.getElementById('to_sum_value').value = null
            document.getElementById('from_sum_value').value = null
            document.getElementById('div_between_sum').style.display = 'none'
            document.getElementById('div_current_sum').style.display = 'block'
        } else if (summ_down === 'В диапазоне') {
            document.getElementById('current_sum_value').value = null
            document.getElementById('div_current_sum').style.display = 'none'
            document.getElementById('div_between_sum').style.display = 'block'

        }
    }


}