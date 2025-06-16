from model.TransaccionRepository import TransaccionRepository


class AnalisisController():
    def __init__(self, usuario, ui):
        self.usuario = usuario
        self.ui = ui
        self.repositorio_transacciones = TransaccionRepository()
        self.cargar_datos()

    def cargar_datos(self):
        self.cargar_resumen_financiero()
        self.mostrar_pie_ingresos_egresos()
        self.mostrar_alertas_exceso_gasto()

    def cargar_resumen_financiero(self):
        ingresos = self.repositorio_transacciones.cargar_transacciones(self.usuario.username, "ingresos")
        egresos = self.repositorio_transacciones.cargar_transacciones(self.usuario.username, "egresos")
        total_ingresos = sum(i.monto for i in ingresos)
        total_egresos = sum(e.monto for e in egresos)
        saldo = total_ingresos - total_egresos
        self.ui.lblSaldoDisponibleAnalisis.setText(f"${saldo:,.2f}")
        self.ui.lblIngresosAnalisis.setText(f"${total_ingresos:,.2f}")
        self.ui.lblEgresosAnalisis.setText(f"${total_egresos:,.2f}")

        # Mostrar porcentaje de ahorro
        if total_ingresos > 0:
            porcentaje_ahorro = (saldo / total_ingresos) * 100
            porcentaje_ahorro = max(0, porcentaje_ahorro)  # No permitir valores negativos
            self.ui.lblPorcentajeAhorro.setText(f"{porcentaje_ahorro:.1f}%")
            self.ui.barraPorcentajeAhorro.setMinimum(0)
            self.ui.barraPorcentajeAhorro.setMaximum(100)
            self.ui.barraPorcentajeAhorro.setValue(int(porcentaje_ahorro))
        else:
            self.ui.lblPorcentajeAhorro.setText("0.0%")
            self.ui.barraPorcentajeAhorro.setMinimum(0)
            self.ui.barraPorcentajeAhorro.setMaximum(100)
            self.ui.barraPorcentajeAhorro.setValue(0)

    def mostrar_pie_ingresos_egresos(self):
        import matplotlib
        matplotlib.use('Agg')  # Evita problemas de backend
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.figure import Figure
        from PyQt6.QtWidgets import QVBoxLayout, QLabel
        from PyQt6.QtCore import Qt

        ingresos = self.repositorio_transacciones.cargar_transacciones(self.usuario.username, "ingresos")
        egresos = self.repositorio_transacciones.cargar_transacciones(self.usuario.username, "egresos")
        total_ingresos = sum(i.monto for i in ingresos)
        total_egresos = sum(e.monto for e in egresos)

        # Elimina gráficos previos
        layout = self.ui.widgetGraficoIngresosEgresos.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
        else:
            layout = QVBoxLayout(self.ui.widgetGraficoIngresosEgresos)
            self.ui.widgetGraficoIngresosEgresos.setLayout(layout)

        if total_ingresos == 0 and total_egresos == 0:
            # Si no hay datos, no mostrar gráfico y mostrar mensaje opcional
            label = QLabel("No hay datos de ingresos ni egresos para mostrar.")
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            layout.addWidget(label)
            return

        fig = Figure(figsize=(3, 3))
        ax = fig.add_subplot(111)
        valores = [total_ingresos, total_egresos]
        etiquetas = ['Ingresos', 'Egresos']
        colores = ['#4CAF50', '#F44336']
        ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', colors=colores, startangle=90)
        ax.set_title('Ingresos vs Egresos')
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

    def mostrar_alertas_exceso_gasto(self):
        from PyQt6.QtWidgets import QVBoxLayout
        from view.AlertaWidget import AlertaWidget
        from model.PresupuestoRepository import PresupuestoRepository
        import datetime

        # Limpiar alertas previas
        layout = self.ui.widgetAlertas.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
        else:
            layout = QVBoxLayout(self.ui.widgetAlertas)
            self.ui.widgetAlertas.setLayout(layout)

        # Obtener mes y año actual
        hoy = datetime.date.today()
        mes = str(hoy.month).zfill(2)  # Formato '06'
        anio = str(hoy.year)           # Formato '2025'

        # Obtener presupuestos y egresos por categoría
        repo_presupuesto = PresupuestoRepository()
        try:
            presupuestos = repo_presupuesto.cargar_presupuesto_mensual(self.usuario.username, mes, anio).presupuestos
        except FileNotFoundError:
            presupuestos = []
        egresos_por_categoria = self.repositorio_transacciones.obtener_egresos_por_usuario_y_mes(self.usuario.username, mes, anio)

        # Alerta: Exceso de gasto en categoría
        for presupuesto in presupuestos:
            cat_id = presupuesto.categoria.id
            monto_presupuestado = presupuesto.monto_objetivo
            monto_egresado = egresos_por_categoria.get(cat_id, 0)
            if monto_egresado > monto_presupuestado:
                mensaje = f"Has gastado ${monto_egresado:,.2f} en '{presupuesto.categoria.nombre}', superando tu presupuesto de ${monto_presupuestado:,.2f}."
                alerta = AlertaWidget("gasto_presupuesto", mensaje, "alto")
                layout.addWidget(alerta)

        # Alerta: Saldo bajo
        ingresos = self.repositorio_transacciones.cargar_transacciones(self.usuario.username, "ingresos")
        egresos = self.repositorio_transacciones.cargar_transacciones(self.usuario.username, "egresos")
        total_ingresos = sum(i.monto for i in ingresos)
        total_egresos = sum(e.monto for e in egresos)
        saldo = total_ingresos - total_egresos
        if saldo < 100:  # Umbral configurable
            mensaje = f"Tu saldo disponible es bajo: ${saldo:,.2f}. Considera reducir tus gastos."
            alerta = AlertaWidget("saldo_bajo", mensaje, "alto")
            layout.addWidget(alerta)

        # Alerta: Ahorro insuficiente
        ahorro = total_ingresos - total_egresos
        if total_ingresos > 0:
            porcentaje_ahorro = ahorro / total_ingresos
            if porcentaje_ahorro < 0.1:  # Menos del 10% de ahorro
                mensaje = f"Solo has ahorrado el {porcentaje_ahorro*100:.1f}% de tus ingresos este mes. Intenta ahorrar al menos el 10%."
                alerta = AlertaWidget("ahorro_bajo", mensaje, "medio")
                layout.addWidget(alerta)
