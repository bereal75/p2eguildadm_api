from sqlalchemy import Table, MetaData
from sqlalchemy.sql import text
from sqlalchemy_views import CreateView, DropView


from .database import Base

view = Table('v_gamelogsr_extended', MetaData())
definition = 'select g.log_dts,'\
	            'to_char(g.log_dts,'\
                ''''yyyy-mm-dd''''::text)::date as log_date,'\
                'g.walletid, '\
                'w.personid,'\
                'w.alias, '\
                'g.pending_earnings, '\
                'g.total_earnings, '\
                'g.current_energy, '\
                'g.max_energy, '\
	            'row_number() over (partition by g.walletid, to_char(g.log_dts, ''''yyyy-mm-dd''''::text)::date order by g.log_dts desc  ) as RowNumLog,'\
	            'row_number() over (partition by g.walletid order by g.log_dts desc  ) as RowNumLatestLog'\
        'from '\
            'public.gamelogsr g '\
            'join public.v_wallets_extended w  '\
                'on w.walletid  = g.walletid") '
create_view= CreateView(view, text(definition))
